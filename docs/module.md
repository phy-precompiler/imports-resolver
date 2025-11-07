# Table of Contents

* [phy\_imports\_resolver](#phy_imports_resolver)
  * [resolve](#phy_imports_resolver.resolve)

<a id="phy_imports_resolver"></a>

# phy\_imports\_resolver

Resolve imports of a python file or module, exclude site packages & builtin modules.

<a id="phy_imports_resolver.resolve"></a>

#### resolve

```python
def resolve(entry_file: Path,
            project_dir: Path = None) -> FileModuleImportsNode | None
```

Resolve imports from entry code file, within given search directory. If no search directory is
given, current work directory is used.

