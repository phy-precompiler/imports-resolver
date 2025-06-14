""" types to describe import relationship among modules """
# imports
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import List, Tuple, Optional

# local imports
from phy_imports_resolver._extractor import extract_import_ast_nodes, ImportUnionAst


# constants

# Search for python code file with these file suffixes by module name. 
# TODO: replace to ('.phy', ) when release
SEARCH_FOR_SUFFIXES: Tuple[str, ...] = ('.py', '.pyi')


@dataclass
class Module:
    """ Like builtin `module` object but in parsing time instead of runtime. """
    name: str
    path: Path

    def __hash__(self):
        """ make hashable """
        return hash(self.path)


@dataclass
class ModuleFile(Module):
    """ module as single file, with file name the same as module name """

    def extract_import_ast(self) -> List[ImportUnionAst]:
        """ extract import ast node from module file """
        return extract_import_ast_nodes(self.path)
    
    @classmethod
    def create_or_null(cls, name: str, path: Path) -> Optional['ModuleFile']:
        """ validate before create instance; if failed, return None """
        if path.exists() and path.is_file():
            return cls(name=name, path=path)
        return None
    
    @classmethod
    def create_or_err(cls, name: str, path: Path) -> Optional['ModuleFile']:
        """ validate before create instance; if failed, raise error """
        if path.exists() and path.is_file():
            return cls(name=name, path=path)
        raise FileNotFoundError(str(path))
    
    def __hash__(self):
        """ make hashable """
        return super().__hash__()


@dataclass
class ModulePackage(Module):
    """ Module as packages, with folder name the same as module name and a `__init__` file.
    
    Notice that builtin `module.__path__` is a list instead of single file, intended to be designed 
    for `native namespace package`, which is not unnessary to take into account here for different native 
    namesapce packages cannot coexists in same project folder.
    """
    @property
    def dunder_init_path(self) -> Optional[Path]:
        """ `__init__.*` file of the package """
        for _suffix in SEARCH_FOR_SUFFIXES:
            dunder_init_file = self.path / ('__init__' + _suffix)
            if dunder_init_file.exists() and dunder_init_file.is_file():
                return dunder_init_file
        
        # dunder init file may not exists in cases of `native namespace package`
        return None
    
    @classmethod
    def create_or_null(cls, name: str, path: Path) -> Optional['ModuleFile']:
        """ validate before create instance; if failed, return None """
        if path.exists() and path.is_dir():
            return cls(name=name, path=path)
        return None
    
    @classmethod
    def create_or_err(cls, name: str, path: Path) -> Optional['ModuleFile']:
        """ validate before create instance; if failed, raise error """
        if path.exists() and path.is_dir():
            return cls(name=name, path=path)
        raise FileNotFoundError(str(path))
    
    def __hash__(self):
        """ make hashable """
        return super().__hash__()


@dataclass
class ModuleImportsNode:
    """ module with dependent imports info """
    mod: Module

    # Project is the directory that look for python modules, it is usually the current work directory.
    # It is essential for resolving imports; if imported module is outside of the project directory, it 
    # will not be resolved and be regarded as site-packages.
    project_dir: Path
    imports: List['ModuleImportsNode']  # DO NOT use `Self` for it is introduced until 3.11
    code: Optional[str] = None  # import statement code

    @property
    def name(self) -> str:
        """ getter of `name` """
        return self.mod.name
    
    @property
    def path(self) -> Path:
        """ getter of `path` """
        return self.mod.path

    def repr_element(self) -> ET.Element:
        """ represent the ast node as xml-like node """
        # use relative path to project directory to simplify the output
        simplified_path = self.path.relative_to(self.project_dir)
        root = ET.Element('module', name=self.name, path=str(simplified_path))

        if self.code:
            root.set('code', self.code)
        
        if self.imports:
            imports_et = ET.Element('imports')
            for import_node in self.imports:
                imports_et.append(import_node.repr_element())
            root.append(imports_et)

        return root
    
    def _stringify_repr_element(self) -> str:
        """ print element tree with indent xml-like format """
        root = self.repr_element()
        ET.indent(root, space=' ' * 2, level=0)
        return ET.tostring(root, encoding='unicode', method='xml')
    
    def __str__(self) -> str:
        """ Both `__str__` & `__repr__` should be explicitly defined, or the subclass
        may call `object.__str__()` or `obejct.__repr__()`. """
        return self._stringify_repr_element()

    def __repr__(self):
        """ Both `__str__` & `__repr__` should be explicitly defined, or the subclass
        may call `object.__str__()` or `obejct.__repr__()`. """
        return self._stringify_repr_element()


# pylint: disable=useless-parent-delegation
@dataclass
class FileModuleImportsNode(ModuleImportsNode):
    """ module of single file with dependent imports info """
    mod: ModuleFile

    def repr_element(self) -> ET.Element:
        root = super().repr_element()
        root.tag = 'file'
        return root
    
    def __str__(self):
        return super().__str__()
    
    def __repr__(self):
        return super().__repr__()


# pylint: disable=useless-parent-delegation
@dataclass
class PackageModuleImportsNode(ModuleImportsNode):
    """ module of single file with dependent imports info """
    mod: ModulePackage

    def repr_element(self) -> ET.Element:
        root = super().repr_element()
        root.tag = 'package'
        return root
    
    def __str__(self):
        return super().__str__()
    
    def __repr__(self):
        return super().__repr__()
