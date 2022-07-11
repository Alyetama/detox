# detox

- `detox`[^1] is a Python tool that can be used to rename directories/files with unsafe characters or spaces.

## Requirements

- [Python>=3.6](https://www.python.org/downloads/)

## Installation

```shell
pip install -U detoxpy
```

## Usage

```
usage: detox [-h] [-r] [-R REPLACE_WITH] [-t] [-l] [-n] [-p] path [path ...]

positional arguments:
  path                  Path to a single or multiple files/directories to detox

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       Rename files recursively
  -R REPLACE_WITH, --replace-with REPLACE_WITH
                        Replace spaces and unsafe characters with this character (default: '_')
  -t, --keep-trailing   Keep the trailing character if exists (e.g., 'foo_')
  -l, --keep-leading    Keep the leading character if exists (e.g., '_foo')
  -n, --dry-run         Do a trial run with no permanent changes
  -p, --plain-print     Print the change as plain text
```

## Examples

### Example 1: Detox a single file/directory:

```shell
detox '(foo)^bar.txt'
# '(foo)^bar.txt' --> 'foo_bar.txt'

detox 'foo&bar/'
# 'foo&bar' --> 'foo_bar'
```

### Example 2: Detox a directory recursively:

```shell
# foo bar
# └── foo1&foo2
#     ├── foo bar (copy 1).jpg
#     └── foo bar (copy 2).jpg

detox -r 'foo bar'

# foo_bar
# └── foo1_foo2
#     ├── foo_bar_copy_1.jpg
#     └── foo_bar_copy_2.jpg
```

### Example 3: Duplicate names after detoxing

- `detox` will avoid overwriting if the detoxed name already exists. For example:

```shell
tree 'foo foo'
# foo foo
#   ├── foo^bar.jpg
#   └── foo%bar.jpg

detox -r -i 'foo foo'

# foo_foo
#   ├── foo_bar.jpg
#   └── foo_bar-1.jpg
```

[^1]: The name is inspired by the tool [detox](https://linux.die.net/man/1/detox)
