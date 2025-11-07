# Table of Contents

* [phy\_imports\_resolver.types](#phy_imports_resolver.types)
  * [Module](#phy_imports_resolver.types.Module)
  * [ModuleFile](#phy_imports_resolver.types.ModuleFile)
    * [extract\_import\_ast](#phy_imports_resolver.types.ModuleFile.extract_import_ast)
    * [create\_or\_null](#phy_imports_resolver.types.ModuleFile.create_or_null)
    * [create\_or\_err](#phy_imports_resolver.types.ModuleFile.create_or_err)
  * [ModulePackage](#phy_imports_resolver.types.ModulePackage)
    * [get\_submod](#phy_imports_resolver.types.ModulePackage.get_submod)
    * [get\_submod\_file](#phy_imports_resolver.types.ModulePackage.get_submod_file)
    * [get\_submod\_pkg](#phy_imports_resolver.types.ModulePackage.get_submod_pkg)
    * [dunder\_init\_mod\_file](#phy_imports_resolver.types.ModulePackage.dunder_init_mod_file)
    * [is\_native\_namespace](#phy_imports_resolver.types.ModulePackage.is_native_namespace)
    * [create\_or\_null](#phy_imports_resolver.types.ModulePackage.create_or_null)
    * [create\_or\_err](#phy_imports_resolver.types.ModulePackage.create_or_err)
  * [ModuleImportsNode](#phy_imports_resolver.types.ModuleImportsNode)
    * [imports](#phy_imports_resolver.types.ModuleImportsNode.imports)
    * [code](#phy_imports_resolver.types.ModuleImportsNode.code)
    * [\_\_init\_\_](#phy_imports_resolver.types.ModuleImportsNode.__init__)
    * [name](#phy_imports_resolver.types.ModuleImportsNode.name)
    * [path](#phy_imports_resolver.types.ModuleImportsNode.path)
    * [repr\_element](#phy_imports_resolver.types.ModuleImportsNode.repr_element)
    * [\_\_repr\_\_](#phy_imports_resolver.types.ModuleImportsNode.__repr__)
  * [FileModuleImportsNode](#phy_imports_resolver.types.FileModuleImportsNode)
  * [PackageModuleImportsNode](#phy_imports_resolver.types.PackageModuleImportsNode)

<a id="phy_imports_resolver.types"></a>

# phy\_imports\_resolver.types

types to describe import relationship among modules

<a id="phy_imports_resolver.types.Module"></a>

## Module Objects

```python
@dataclass
class Module()
```

Like builtin `module` object but in parsing time instead of runtime.

<a id="phy_imports_resolver.types.ModuleFile"></a>

## ModuleFile Objects

```python
@dataclass
class ModuleFile(Module)
```

module as single file, with file name the same as module name

<a id="phy_imports_resolver.types.ModuleFile.extract_import_ast"></a>

#### extract\_import\_ast

```python
def extract_import_ast() -> List[ImportUnionAst]
```

extract import ast node from module file

<a id="phy_imports_resolver.types.ModuleFile.create_or_null"></a>

#### create\_or\_null

```python
@classmethod
def create_or_null(cls, name: str, path: Path) -> Optional['ModuleFile']
```

validate before create instance; if failed, return None

<a id="phy_imports_resolver.types.ModuleFile.create_or_err"></a>

#### create\_or\_err

```python
@classmethod
def create_or_err(cls, name: str, path: Path) -> Optional['ModuleFile']
```

validate before create instance; if failed, raise error

<a id="phy_imports_resolver.types.ModulePackage"></a>

## ModulePackage Objects

```python
@dataclass
class ModulePackage(Module)
```

Module as packages, with folder name the same as module name and a `__init__` file.

Notice that builtin `module.__path__` is a list instead of single file, intended to be designed 
for `native namespace package`, which is not unnessary to take into account here for different native 
namesapce packages cannot coexists in same project folder.

<a id="phy_imports_resolver.types.ModulePackage.get_submod"></a>

#### get\_submod

```python
def get_submod(submod_name: str) -> Optional[Module]
```

find submodule of the package

<a id="phy_imports_resolver.types.ModulePackage.get_submod_file"></a>

#### get\_submod\_file

```python
def get_submod_file(submod_name: str) -> Optional[ModuleFile]
```

find file submodule of the package

<a id="phy_imports_resolver.types.ModulePackage.get_submod_pkg"></a>

#### get\_submod\_pkg

```python
def get_submod_pkg(submod_name: str) -> Optional['ModulePackage']
```

find package submodule of the package

<a id="phy_imports_resolver.types.ModulePackage.dunder_init_mod_file"></a>

#### dunder\_init\_mod\_file

```python
@property
def dunder_init_mod_file() -> Optional[ModuleFile]
```

`__init__.*` file of the package

<a id="phy_imports_resolver.types.ModulePackage.is_native_namespace"></a>

#### is\_native\_namespace

```python
@property
def is_native_namespace() -> bool
```

dunder init file may not exists when self is `native namespace package`

<a id="phy_imports_resolver.types.ModulePackage.create_or_null"></a>

#### create\_or\_null

```python
@classmethod
def create_or_null(cls, name: str, path: Path) -> Optional['ModulePackage']
```

validate before create instance; if failed, return None

<a id="phy_imports_resolver.types.ModulePackage.create_or_err"></a>

#### create\_or\_err

```python
@classmethod
def create_or_err(cls, name: str, path: Path) -> Optional['ModulePackage']
```

validate before create instance; if failed, raise error

<a id="phy_imports_resolver.types.ModuleImportsNode"></a>

## ModuleImportsNode Objects

```python
class ModuleImportsNode()
```

module with dependent imports info

<a id="phy_imports_resolver.types.ModuleImportsNode.imports"></a>

#### imports

DO NOT use `Self` for it is introduced until 3.11

<a id="phy_imports_resolver.types.ModuleImportsNode.code"></a>

#### code

import statement code

<a id="phy_imports_resolver.types.ModuleImportsNode.__init__"></a>

#### \_\_init\_\_

```python
def __init__(mod: Module,
             project_dir: Path,
             imports: List['ModuleImportsNode'] = None,
             **kwargs)
```

constructor

<a id="phy_imports_resolver.types.ModuleImportsNode.name"></a>

#### name

```python
@property
def name() -> str
```

getter of `name`

<a id="phy_imports_resolver.types.ModuleImportsNode.path"></a>

#### path

```python
@property
def path() -> Path
```

getter of `path`

<a id="phy_imports_resolver.types.ModuleImportsNode.repr_element"></a>

#### repr\_element

```python
def repr_element() -> ET.Element
```

represent the ast node as xml-like node

<a id="phy_imports_resolver.types.ModuleImportsNode.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__() -> str
```

print element tree with indent xml-like format

<a id="phy_imports_resolver.types.FileModuleImportsNode"></a>

## FileModuleImportsNode Objects

```python
class FileModuleImportsNode(ModuleImportsNode)
```

module of single file with dependent imports info

<a id="phy_imports_resolver.types.PackageModuleImportsNode"></a>

## PackageModuleImportsNode Objects

```python
class PackageModuleImportsNode(ModuleImportsNode)
```

module of single file with dependent imports info

