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
        f.write('# NOTEME\n')
    print('Creating noteme.md file')


def write_lines(lines: list[str]) -> None:
    with open('noteme.md', 'w') as f:
        for line in lines:
            f.write(line)


def mark(indicies: list[int]) -> None:
    with open('noteme.md', 'r+') as f:
        lines = f.readlines()
        try:
            for i in indicies:
                if re.search(r'\[ \]', lines[i]):
                    lines[i] = re.sub(r'\[ \]', '[x]', lines[i])
                else:
                    lines[i] = re.sub(r'\[x\]', '[ ]', lines[i])
        except IndexError as e:
            print(f'{type(e).__name__}: Entry index out of range: {i}')
        write_lines(lines)


def add(note: str) -> None:
    dt = datetime.now()
    fdt = dt.strftime('(_%a %m/%d/%y, %H:%M:%S_ )')

    with open('noteme.md', 'a') as f:
        f.write(f'- [ ] {fdt} - {note}\n')


def remove(indicies: list[int]) -> None:
    with open('noteme.md', 'r+') as f:
        lines = f.readlines()
        for i in sorted(indicies, reverse=True):
            try:
                ln = lines[i]
                del lines[i]
                print(f'Removed entry no. {i}: {ln}')
            except IndexError as e:
                print(f'IndexError: {e} ({i})')
        write_lines(lines)


def remove_range(x: int, y: int) -> None:
    with open('noteme.md', 'r+') as f:
        lines = f.readlines()
        index_max = max(range(len(lines)))
        try:
            if x > index_max:
                raise IndexError
            del lines[x: y + 1]
            if x == index_max:
                print(f'Removes entries: {x}')
            else:
                print(f'Removes entries: {x} through {index_max}')
        except IndexError as e:
            read_print_file()
            sys.exit(f'{type(e).__name__}: Entry index out of range: {x} ')
        write_lines(lines)


def read_print_file() -> None:
    with open('noteme.md') as f:
        for i, line in enumerate(f):
            if i == 0:
                print(f'{line}', end='')
            else:
                print(f'{i}\t{line}', end='')


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
        '-rmr', '--removerange',
        help='Remove a todo (range)',
        type=int,
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
        try:
            add(args.add)
            print(f'Added {args.add}')
        except ValueError:
            sys.exit('Note must be contained within quotation marks')

    if args.remove and args.removerange:
        sys.exit(f'Only one of the options (remove or removerange)'
                 f' can be used at one time')

    if args.remove:
        remove(args.remove)

    if args.removerange and not args.remove:
        remove_range(x=int(args.removerange[0]),
                     y=int(args.removerange[1]))

    # if args.add and args.mark:
    #     print(f'{args.add=} {args.mark=}')
    
    if args.mark:
        print(args.mark)
        mark(args.mark)

    read_print_file()

    return 0


if __name__ == '__main__':
    exit(main())
