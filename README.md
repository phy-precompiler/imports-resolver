# Resolve imports of a python file or module, exclude site packages & builtin modules.

# NOTES

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

