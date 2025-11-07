# Table of Contents

* [phy\_imports\_resolver.resolver](#phy_imports_resolver.resolver)
  * [ImportResolver](#phy_imports_resolver.resolver.ImportResolver)
    * [resolved\_mod](#phy_imports_resolver.resolver.ImportResolver.resolved_mod)
    * [\_\_init\_\_](#phy_imports_resolver.resolver.ImportResolver.__init__)
    * [start](#phy_imports_resolver.resolver.ImportResolver.start)

<a id="phy_imports_resolver.resolver"></a>

# phy\_imports\_resolver.resolver

resolve import relationship among modules

<a id="phy_imports_resolver.resolver.ImportResolver"></a>

## ImportResolver Objects

```python
class ImportResolver()
```

resolve importing chain from given entry code file, searching within given project path

<a id="phy_imports_resolver.resolver.ImportResolver.resolved_mod"></a>

#### resolved\_mod

avoid circular imports

<a id="phy_imports_resolver.resolver.ImportResolver.__init__"></a>

#### \_\_init\_\_

```python
def __init__(project_dir: Path = None)
```

Init resolver with project directory.

Project is the directory that look for python modules, it is usually the current work directory.

<a id="phy_imports_resolver.resolver.ImportResolver.start"></a>

#### start

```python
def start(entry_file: Path) -> FileModuleImportsNode | None
```

entry file to start resolving

