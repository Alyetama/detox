# detox[^1]

## Requirements

- [Python>=3.6](https://www.python.org/downloads/)

## Installation

```shell
sh -c "$(curl -fsSL https://raw.githubusercontent.com/Alyetama/detox/main/install.sh)"
```

## Usage

```
usage: detox [-h] -i INPUT [-r] [-u USING] [-t] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the file/folder to rename
  -r, --recursive       Rename files recursively
  -u USING, --using USING
                        Replace spaces and unsafe characters with this
                        character (default: '_')
  -t, --keep-trailing   Keep the trailing character if exists (e.g., 'foo_';
                        default: False)
  -l, --keep-leading    Keep the leading character if exists (e.g., '_foo';
                        default: False)
```

## Examples

- Detox a single file/directory:

```shell
detox -i '(foo)^bar.txt'
# '(foo)^bar.txt' --> 'foo__bar.txt'
```

- Detox a directory recursively:

```shell
# foo bar
# └── foo1&foo2
#     ├── foo bar (copy 1).jpg
#     └── foo bar (copy 2).jpg

detox -r -i 'foo bar'

# foo_bar
# └── foo1_foo2
#     ├── foo_bar__copy_1.jpg
#     └── foo_bar__copy_2.jpg
```

- `detox` avoids overwriting if the detoxed name already exists:

```shell
# foo foo
#   ├── foo^bar.jpg
#   └── foo%bar.jpg

detox -r -i 'foo foo'

# foo_foo
#   ├── foo_bar.jpg
#   └── foo_bar-1.jpg
```

[^1]: The name is inspired by the tool [detox](https://github.com/dharple/detox)
