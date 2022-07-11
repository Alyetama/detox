#!/usr/bin/env python
# coding: utf-8

import os
import shutil
import unittest
from pathlib import Path

from detox import detox


class TestDetox(unittest.TestCase):

    def SetUp(self):
        pass

    def test_simple_detox(self):
        Path('foo bar').mkdir(exist_ok=True)
        bad_basenames = ['foo bar', 'foo%bar', 'foo&bar', 'foo^bar']
        bad_paths = ['foo bar'
                     ] + [f'foo bar/{x}.txt' for x in bad_basenames[1:]]
        good_basenames = ['foo_bar', 'foo_bar', 'foo_bar-1', 'foo_bar-2']
        good_paths = ['foo_bar'
                      ] + [f'foo_bar/{x}.txt' for x in good_basenames[1:]]
        for bad_path in bad_paths:
            Path(bad_path).touch()

        results = detox.Detox('foo bar', recursive=True).run()
        results = [x[1] for x in results]
        for result, expected in zip(results, good_paths):
            self.assertEqual(Path(result), Path(expected))
        shutil.rmtree('foo_bar')

    def test_nested_detox(self):
        bad_nested_parent = 'detox ^& test  # test/make^^f__lgr/msc_{}__!_6__^^___😀 ksm'  # noqa E501
        good_nested_parent = 'detox_test_test/make_f_lgr/msc_6_ksm'
        bad_nested_dir = f"{bad_nested_parent}/$untitled|fff_\&_🚀_'_folder"  # noqa: E501
        good_nested_dir = f'{good_nested_parent}/untitled_fff_folder'
        bad_nested_file = f'{bad_nested_parent}/pypy-😀🚀_^^^_"$_6_🚀.py'  # noqa: E501
        good_nested_file = f'{good_nested_parent}/pypy-_6.py'  # noqa: E501

        Path(bad_nested_dir).mkdir(parents=True)
        Path(bad_nested_file).touch()

        detox.Detox('detox ^& test  # test', recursive=True).run()
        self.assertTrue(Path(good_nested_dir).exists())
        self.assertTrue(Path(good_nested_file).exists())
        shutil.rmtree('detox_test_test')

    def test_detox_with_trailing_path(self):
        Path('foo_').touch()
        result = detox.Detox('foo_', keep_trailing=True).run()
        self.assertFalse(result, [])
        os.remove('foo_')

    def test_detox_with_leading_path(self):
        Path('_foo').touch()
        result = detox.Detox('_foo', keep_leading=True).run()
        self.assertFalse(result, [])
        os.remove('_foo')


if __name__ == '__main__':
    unittest.main()
