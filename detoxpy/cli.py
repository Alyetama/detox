#!/usr/bin/env python
# coding: utf-8

import argparse

from . import detox


def opts() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        nargs='+',
        type=str,
        help='Path to a single or multiple files/directories to detox')
    parser.add_argument('-r',
                        '--recursive',
                        help='Rename files recursively',
                        action='store_true')
    parser.add_argument(
        '-R',
        '--replace-with',
        help='Replace spaces and unsafe characters with this character '
        '(default: \'_\')',
        type=str,
        default='_')
    parser.add_argument(
        '-t',
        '--keep-trailing',
        help='Keep the trailing character if exists (e.g., \'foo_\')',
        action='store_true')
    parser.add_argument(
        '-l',
        '--keep-leading',
        help='Keep the leading character if exists (e.g., \'_foo\')',
        action='store_true')
    parser.add_argument('-n',
                        '--dry-run',
                        help='Do a trial run with no permanent changes',
                        action='store_true')
    parser.add_argument('-p',
                        '--plain-print',
                        help='Print the change as plain text',
                        action='store_true')
    return parser.parse_args()


def main():
    args = opts()
    d = detox.Detox(path=args.path,
                    recursive=args.recursive,
                    dry_run=args.dry_run,
                    replace_with=args.replace_with,
                    keep_trailing=args.keep_trailing,
                    keep_leading=args.keep_leading,
                    plain_print=args.plain_print)
    d.run()


if __name__ == '__main__':
    main()
