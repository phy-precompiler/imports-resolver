# Resolve imports of a python file or module, exclude site packages & builtin modules.


## commands

install production + development dependencies:

```shell
poetry install --with dev
```


generate a helper parser for import statement:

```shell
python -m pegen tests/imports.gram -o tests/imports_parser.py
```


run all test:
```shell
poetry run pytest -s
```