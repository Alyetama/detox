#!/usr/bin/env python
# coding: utf-8

import argparse
import re
import os
import string
from pathlib import Path


def detox(_input):
    basename = Path(_input).name
    exclude = ''.join([
        x for x in string.punctuation + string.whitespace
        if x not in list('-_.')
    ])
    new_name = re.sub(fr"[{exclude}]", args.using, basename)

    if not args.keep_trailing and Path(new_name).stem.endswith(args.using):
        new_name = f'{Path(new_name).stem[:-1]}{Path(new_name).suffix}'
    if not args.keep_leading and new_name.startswith(args.using):
        new_name = new_name[1:]

    return new_name


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
        help='Keep the leading character if exists (e.g., \'_foo\'; default: False)',
        action='store_true')
    return parser.parse_args()


def process(subdir, item):
    old_name = Path(subdir) / item
    new_name = Path(subdir) / detox(item)
    if Path(new_name).exists():
        basename = Path(new_name).stem
        suffix = Path(new_name).suffix
        i = 1
        while True:
            new_name = Path(subdir) / f'{basename}-{i}{suffix}'
            if not Path(new_name).exists():
                break
            else:
                i += 1

    if old_name != new_name:
        print(f'\33[31m\'{old_name}\'\x1b[0m --> \33[32m\'{new_name}\'\x1b[0m')
    return old_name, new_name



def main():
    if args.recursive:
        if not Path(args.input).is_dir():
            raise ValueError(
                'The `--recursive` flag requires a directory input not a file!'
            )
        for subdir, dirs, files in os.walk(args.input, topdown=False):
            if files:
                for file in files:
                    old_file, new_file = process(subdir, file)
                    os.rename(old_file, new_file)

            if dirs:
                for _dir in dirs:
                    old_dir, new_dir = process(subdir, _dir)
                    os.rename(old_dir, new_dir)

    os.rename(args.input, Path(args.input).parent / detox(args.input))


if __name__ == '__main__':
    args = opts()
    main()
