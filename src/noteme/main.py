import argparse
import re
from pathlib import Path


def create_markdown_file():
    p = Path('noteme.md')
    if not p.is_file():
        with open('noteme.md', 'w') as f:
            f.write('# NOTEME\n')
        print('Creating noteme.md file')
    else:
        print('noteme.md already exists')



def write_lines(lines: list[str]) -> None:
    with open('noteme.md', 'w') as f:
        for line in lines:
            f.write(line)


def mark(indicies: list[int]) -> None:
    with open('noteme.md', 'r+') as f:
        lines = f.readlines()
        for i in indicies:
            if re.search(r'\[ \]', lines[i]):
                lines[i] = re.sub(r'\[ \]', '[x]', lines[i])
            else:
                lines[i] = re.sub(r'\[x\]', '[ ]', lines[i])
        write_lines(lines)


def append_note(note: str) -> None:
    with open('noteme.md', 'a') as f:
        f.write(f'- [ ] {note}\n')


def remove(indicies: list[int]) -> None:
    with open('noteme.md', 'r+') as f:
        lines = f.readlines()
        for i in sorted(indicies):
            del lines[i]
        write_lines(lines)


def remove_range(x: int, y: int) -> None:
    with open('noteme.md', 'r+') as f:
        lines = f.readlines()
        del lines[x: y + 1]
        write_lines(lines)


def read_print_file() -> None:
    with open('noteme.md', 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                print(f'{line}', end='')
            else:
                print(f'  {i}\t{line}', end='')


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Todo accesible anywhere in your terminal',
        usage='%(prog)s [options]'
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
        '-rmr', '--removerange',
        help='Remove a todo (range)',
        nargs=2,
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

    args = parser.parse_args()

    if args.create:
        create_markdown_file()
    if args.add:
        append_note(args.add)
        print(f'Added {args.add}')
    if args.remove:
        remove(args.remove)
        print(f'Removed {args.remove}')
    if args.removerange:
        remove_range(x=int(args.removerange[0]), y=int(args.removerange[1]))
        print(f'Removed {args.removerange[0]} - {args.removerange[1]}')
    if args.mark:
        mark(args.mark)
        print(f'Updated {args.mark}')

    read_print_file()


if __name__ == '__main__':
    main()
