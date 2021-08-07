import argparse
import re
import sys
from datetime import datetime


def create_markdown_file() -> None:
    try:
        open('noteme.md', 'x')
    except FileExistsError:
        sys.exit('noteme.md already exists')
    with open('noteme.md', 'w') as f:
        f.write('### Todo\n### In Progress\n### Completed\n')
    print('Creating noteme.md file')


def write_lines(lines: list[str]) -> None:
    with open('noteme.md', 'w') as f:
        for line in lines:
            f.write(line)


def mark(entry: str, mark: bool) -> str:
    if mark:
        entry = re.sub(r'\[ \]', '[x]', entry)
    else:
        entry = re.sub(r'\[x\]', '[ ]', entry)

    return entry


def add(note: str) -> None:
    dt = datetime.now()
    fdt = dt.strftime('(_%a %m/%d/%y, %H:%M:%S_ )')
    entry = f'- [ ] {fdt} - {note}\n'

    with open('noteme.md', 'r+') as f:
        lines = f.readlines()
    try:
        in_progress_index = lines.index(f'### In Progress\n')
        lines.insert(in_progress_index, entry)
        write_lines(lines)
        print(f'Added: {note}')
    except Error as e:
        print(f'{type(e).__name__}: {e}')


def remove(lns: list[int]) -> None:
    with open('noteme.md', 'r+') as f:
        lines = f.readlines()
    entries = [x for x in lines if x.startswith('-')]
    for ln in sorted(lns, reverse=True):
        try:
            entry = entries[ln]
            entry_index = lines.index(entry)
            del lines[entry_index]
            print(f'Removed entry no. {ln}: {entry}')
        except IndexError as e:
            print(f'IndexError: {e}: {ln}')
    write_lines(lines)

def move(lns: list[int], complete: bool = False) -> None:
    with open('noteme.md', 'r+') as f:
        lines = f.readlines()
    try:
        print(f'{complete=}')
        in_progress_index = lines.index(f'### In Progress\n')
        completed_index = lines.index(f'### Completed\n')
        entries = [x for x in lines if x.startswith('-')]
        for ln in lns:
            entry = entries[ln]
            pos = lines.index(entry)
            if complete:
                # -m Flag selected
                if pos > completed_index:
                    # Marked as completed. Unmark and move to 'Todo'
                    del lines[pos]
                    unmarked_entry = mark(entry, mark=False)
                    lines.insert(in_progress_index, unmarked_entry)
                else:
                    # Not marked as completed. Mark and move to 'Completed'
                    del lines[pos]
                    marked_entry = mark(entry, mark=True)
                    lines.append(marked_entry)
            elif pos > in_progress_index and pos < completed_index:
                # Move to 'Todo'
                del lines[pos]
                lines.insert(in_progress_index, entry)
            else:
                # Move to 'In Progress'
                del lines[pos]
                lines.insert(completed_index-1, entry)

    except IndexError as e:
            print(f'{type(e).__name__}: Entry index out of range: {ln}')

    write_lines(lines)


def read_print_file() -> None:
    with open('noteme.md') as f:
        i = 0
        for line in f:
            if line[0] == '#' or len(line.strip()) == 0:
                print(f'{line}', end='')
            else:
                print(f'{i}\t{line}', end='')
                i += 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Todo accesible anywhere in your terminal',
        usage='%(prog)s [options]',
    )
    parser.add_argument(
        '-a', '--add',
        help='Add a todo',
        type=str,
        nargs='?',
    )
    parser.add_argument(
        '-rm', '--remove',
        help='Remove a todo',
        type=int,
        nargs='*',
    )
    parser.add_argument(
        '-m', '--mark',
        help='Change checkmark status',
        type=int,
        nargs='*',
    )
    parser.add_argument(
        '-c', '--create',
        help='Create a note markdown file',
        action='store_true',
    )
    parser.add_argument(
        '-p', '--progress',
        help='Move in and out of In Progress',
        type=int,
        nargs='*',
    )

    args = parser.parse_args()

    if args.create:
        create_markdown_file()

    if args.add:
        try:
            add(args.add)
        except ValueError:
            sys.exit('Note must be contained within quotation marks')

    if args.remove:
        remove(args.remove)

    if args.mark:
        move(args.mark, True)

    if args.progress:
        move(args.progress)

    read_print_file()

    return 0


if __name__ == '__main__':
    exit(main())
