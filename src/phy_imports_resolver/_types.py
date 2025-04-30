""" typings & related methods """
# imports
from typing import List, TypedDict
from pathlib import Path
from xml.dom.minidom import Document


class ImportPathNode(TypedDict):
    """ json schema for import path tree node """
    path: str
    imports: List['ImportPathNode']


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
