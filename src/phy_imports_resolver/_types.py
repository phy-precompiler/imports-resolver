""" typings & related methods """
# imports
from dataclasses import dataclass
from typing import List, Tuple, Optional
from pathlib import Path
from xml.dom.minidom import Document
import xml.etree.ElementTree as ET


# constants
include_suffixes: Tuple[str, ...] = ('.py', '.pyi')  # TODO: replace to ('.phy', ) when release


@dataclass
class ImportPathNode:
    """ json schema for import path tree node """
    file_path: Path

    # Project is the directory that look for python modules, it is usually the current work directory.
    # It is essential for resolving imports; if imported module is outside of the project directory, it 
    # will not be resolved and be regarded as site-packages.
    project_dir: Path

    imports: List['ImportPathNode']  # DO NOT use `Self` for it is introduced until 3.11

    def repr_element(self) -> ET.Element:
        """ represent the ast node as xml-like node """
        root = ET.Element(self.__class__.__name__, path=str(self.file_path))
        for import_node in self.imports:
            root.append(import_node.repr_element())
        
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


@dataclass
class EntryModNode(ImportPathNode):
    """ entry file as the root of imports tree """
    pass


@dataclass
class FileModNode(ImportPathNode):
    """ python module as a single ".py" file """
    pass


@dataclass
class PackagesModNode(ImportPathNode):
    """ python module as a package, with a "__init__" file """
    
    @property
    def dunder_init_path(self) -> Path:
        """ `__init__` file of the package """
        for _suffix in include_suffixes:
            dunder_init_file = self.file_path / ('__init__' + _suffix)
            if dunder_init_file.exists() and dunder_init_file.is_file():
                return dunder_init_file
            
        raise FileNotFoundError(str(self.file_path))

def print_xml_formatted_import_tree(import_tree: ImportPathNode) -> str:
    """ print import path tree as xml for a clear style """
    # simplify node path as relative one against root path
    entry_path = Path(import_tree['path']).resolve()
    if entry_path.is_file():
        entry_path = entry_path.parent.resolve()

    doc = Document()

    # process node recursively
    def _node_to_xml(node: ImportPathNode, is_root: bool, doc: Document = doc, entry_path: Path = entry_path):
        element = doc.createElement('entry' if is_root else 'import')
        node_path = Path(node['path']).resolve()

        if not is_root:
            try:
                node_path = node_path.relative_to(entry_path)
            except ValueError:
                pass

        element.setAttribute('path', str(node_path))
        
        for import_node in node['imports']:
            import_element = _node_to_xml(import_node, False, doc, entry_path=entry_path)
            element.appendChild(import_element)

        return element
    
    root_element = _node_to_xml(import_tree, True, doc=doc, entry_path=entry_path)
    doc.appendChild(root_element)
    return doc.toprettyxml(indent=' '* 2)  # two spaces as indent
