#!/usr/bin/env python
# coding: utf-8

import os
import re
import string
from pathlib import Path
from typing import List, Optional, Union, Tuple


class Detox:

    def __init__(self,
                 path: Union[List[str], Path, str],
                 recursive: bool = False,
                 replace_with: str = '_',
                 keep_trailing: bool = False,
                 keep_leading: bool = False,
                 dry_run: bool = False,
                 plain_print: bool = False) -> None:
        self.path = [path] if not isinstance(path, list) else path
        self.recursive = recursive
        self.replace_with = replace_with
        self.keep_trailing = keep_trailing
        self.keep_leading = keep_leading
        self.dry_run = dry_run
        self.plain_print = plain_print

    def _detox_path(self, _input: Union[str, Path]) -> Optional[Path]:
        basename = Path(_input).name
        exclude = ''.join([
            x for x in string.punctuation + string.whitespace
            if x not in list('-_.')
        ])
        printable_name = ''.join([
            x if x in string.printable else self.replace_with for x in basename
        ])
        new_name = re.sub(fr"[{exclude}]", self.replace_with, printable_name)
        new_name = new_name.replace('\\', self.replace_with)

        duplicates_pattern = rf'{self.replace_with}{{2,}}'
        new_name = re.sub(duplicates_pattern, self.replace_with, new_name)

        if not self.keep_trailing:
            new_name = new_name.rstrip(self.replace_with)
            new_name = f'{Path(new_name).stem.rstrip(self.replace_with)}{Path(new_name).suffix}'  # noqa: E501
        if not self.keep_leading:
            new_name = new_name.lstrip(self.replace_with)
            new_name = f'{Path(new_name).stem.lstrip(self.replace_with)}{Path(new_name).suffix}'  # noqa: E501

        if new_name != basename:
            return Path(new_name)

    def _dedupe(self, root: Union[Path, str],
                item: str) -> Optional[Tuple[Path, Path]]:
        if not Path(item).is_file():
            old_name = Path(root) / Path(item)
        else:
            old_name = item
        detoxed = self._detox_path(item)
        if not detoxed:
            return
        new_name = Path(root) / Path(detoxed)
        if Path(new_name).exists():
            basename = Path(new_name).stem
            suffix = Path(new_name).suffix
            i = 1
            while True:
                new_name = Path(root) / Path(f'{basename}-{i}{suffix}')
                if not Path(new_name).exists():
                    break
                else:
                    i += 1
        return old_name, new_name

    def _check_exists(self):
        for path in self.path:
            if not Path(path).exists():
                raise ValueError(f'Path {path} does not exist!')

    def run(self) -> List[Tuple[Path, Path]]:
        self._check_exists()

        input_dirs = [x for x in self.path if Path(x).is_dir()]
        changes = []

        if self.recursive:
            if self.dry_run:
                print(
                    'NOTICE: If multiple files have the same detoxed name, '
                    '`--dry-run` won\'t show the handling of existing names. ')
            if not input_dirs:
                raise ValueError(
                    'The `--recursive` flag requires at least one directory '
                    'in the input!')
            for input_dir in input_dirs:
                for root, dirs, files in os.walk(input_dir, topdown=False):
                    if files:
                        for file in files:
                            result = self._dedupe(root, file)
                            if not result:
                                continue
                            old_file, new_file = result
                            if new_file and not self.dry_run:
                                os.rename(old_file, new_file)
                            changes.append((old_file, new_file))

                    if dirs:
                        for _dir in dirs:
                            result = self._dedupe(root, _dir)
                            if not result:
                                continue
                            old_dir, new_dir = result
                            if new_dir and not self.dry_run:
                                os.rename(old_dir, new_dir)
                            changes.append((old_dir, new_dir))

        for input_item in self.path:
            result = self._dedupe(
                Path(input_item).parent,
                Path(input_item).name)
            if not result:
                continue
            old_item, new_item = result
            if not self.dry_run:
                os.rename(old_item, new_item)
            changes.append((old_item, new_item))

        for change in changes:
            if self.plain_print:
                print(change[1].name)
            else:
                print(f'\33[31m\'{change[0].name}\'\x1b[0m --> '
                      f'\33[32m\'{change[1].name}\'\x1b[0m')

        changes = [x for x in changes if Path(x[1]).exists()]
        return changes
