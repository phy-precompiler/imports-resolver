# PHY-resolve-imports

Resolve imports of a python file or module recursively, exclude site packages & builtin modules.

This project is part of [`phy`](https://github.com/phy-precompiler).

## Install

```shell
pip install phy-imports-resolver
```

## How to use

### Use the API

## Reminder

This package DOES NOT support `importlib` to dynamically import modules, for the module imported by `importlib` can be
variable and thus can only be determined at runtime; otherwise, if the the module imported by `importlib` is
constant string, the developer can absolutely use import statement (non-top-placed) instead.
