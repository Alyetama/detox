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
    new_name = re.sub(fr"[{exclude}]", args.character, basename)
    if new_name.endswith(args.character):
        new_name = new_name[:-1]
    if _input != new_name:
        print(f'\33[31m\'{basename}\'\x1b[0m --> \33[32m\'{new_name}\'\x1b[0m')
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
    parser.add_argument('-c',
                        '--character',
                        help='Replace spaces and unsafe characters with this character (default: _)',
                        type=str,
                        default='_')
    return parser.parse_args()


def main():
    if args.recursive:
        if not Path(args.input).is_dir():
            raise ValueError(
                'The `--recursive` flag requires a directory input not a file!'
            )
        for subdir, dirs, files in os.walk(args.input, topdown=False):
            if files:
                for file in files:
                    os.rename(Path(subdir) / file, Path(subdir) / detox(file))
            if dirs:
                for _dir in dirs:
                    os.rename(Path(subdir) / _dir, Path(subdir) / detox(_dir))

    os.rename(args.input, Path(args.input).parent / detox(args.input))


if __name__ == '__main__':
    args = opts()
    main()
