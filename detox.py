#!/usr/bin/env python
# coding: utf-8

import argparse
import re
import os
import string
from pathlib import Path


def print_change(pre, post):
    print(f'\33[31m\'{Path(pre).name}\'\x1b[0m --> \33[32m\'{Path(post).name}\'\x1b[0m')


def detox(_input):
    basename = Path(_input).name
    exclude = ''.join([
        x for x in string.punctuation + string.whitespace
        if x not in list('-_.')
    ])
    new_name = re.sub(fr"[{exclude}]", args.using, basename)
    if new_name == basename:
        return

    if not args.keep_trailing and Path(new_name).stem.endswith(args.using):
        new_name = f'{Path(new_name).stem[:-1]}{Path(new_name).suffix}'
    if not args.keep_leading and new_name.startswith(args.using):
        new_name = new_name[1:]
    return new_name


def process(root, item):
    old_name = Path(root) / item
    detoxed = detox(item)
    if not detoxed:
        return (None, None)
    new_name = Path(root) / detoxed
    if Path(new_name).exists():
        basename = Path(new_name).stem
        suffix = Path(new_name).suffix
        i = 1
        while True:
            new_name = Path(root) / f'{basename}-{i}{suffix}'
            if not Path(new_name).exists():
                break
            else:
                i += 1
    if old_name != new_name:
        print_change(old_name, new_name)
    return old_name, new_name


def opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',
                        '--input',
                        help='Path to the file/folder to rename',
                        type=str,
                        required=True)
    parser.add_argument('-r',
                        '--recursive',
                        help='Rename files recursively',
                        action='store_true')
    parser.add_argument('-u',
                        '--using',
                        help='Replace spaces and unsafe characters with this '
                        'character (default: \'_\')',
                        type=str,
                        default='_')
    parser.add_argument(
        '-t',
        '--keep-trailing',
        help=
        'Keep the trailing character if exists (e.g., \'foo_\'; default: False)',
        action='store_true')
    parser.add_argument(
        '-l',
        '--keep-leading',
        help=
        'Keep the leading character if exists (e.g., \'_foo\'; default: False)',
        action='store_true')
    parser.add_argument(
        '-n',
        '--dry-run',
        help='Do a trial run with no permanent changes',
        action='store_true')
    return parser.parse_args()


def main():
    if args.recursive:
        if args.dry_run:
            print('NOTICE: If multiple files have the same detoxed name, `--dry-run` won\'t show the handling of existing names.')
        if not Path(args.input).is_dir():
            raise ValueError(
                'The `--recursive` flag requires a directory input, not a file!'
            )
        for root, dirs, files in os.walk(args.input, topdown=False):
            if files:
                for file in files:
                    old_file, new_file = process(root, file)
                    if not args.dry_run and (old_file, new_file) != (None, None):
                        s.rename(old_file, new_file)

            if dirs:
                for _dir in dirs:
                    old_dir, new_dir = process(root, _dir)
                    if not args.dry_run and (old_file, new_file) != (None, None):
                        os.rename(old_dir, new_dir)

    if Path(Path(args.input).parent / detox(args.input)).exists():
        raise FileExistsError('A file with the new name already exists!')

    old_item, new_item = args.input, Path(args.input).parent / detox(args.input)
    print_change(old_item, new_item)

    if not args.dry_run:
        os.rename(_old_name, _new_name)


if __name__ == '__main__':
    args = opts()
    main()
