# Resolve imports of a python file or module, exclude site packages & builtin modules.

# NOTES

+ DO NOT support `importlib` to dynamically import modules, for the module imported by `importlib` can be
variable and thus can only be determined at runtime; otherwise, if the the module imported by `importlib` is
constant string, the developer can absolutely use import statement (non-top-placed) instead.

+ Use python builtin tokenizer to handle code encoding issues; DO NOT handle it by yourself.


## commands

install production + development dependencies:

```shell
poetry install --with dev
```


run all test:
```shell
poetry run pytest -s
```

