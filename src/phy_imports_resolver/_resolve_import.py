""" resolve import node to the path of file module or package """
# imports
import os
import ast as builtin_ast
from pathlib import Path
from typing import Tuple, Optional, Union, List, Set

# local imports
from phy_imports_resolver._extractor import extract_import_ast_nodes
from phy_imports_resolver._types import ImportPathNode


def _resolve_import_name(
    import_name: str,
    find_path: Path, 
    include_suffixes: Tuple[str, ...] = ('.py', '.pyi')  # TODO: replace to ('.phy', ) when release
) -> Optional[Path]:
    """ Resolve import name into path of python module or package. 

    Argument `find_path` can be cwd, or other path that added to PYTHONPATH, but with stdlib path & 
    site-packaegs path exclueded.
    Import name should be absolute, no relative symbol '.' or '..' is allowed.
    """
    # assert the import name is not relative
    assert not import_name.startswith('.')

    # dotted_name '.' NAME | NAME
    import_path = import_name.replace('.', os.sep)

    # imported is package; return __init__ file path
    absolute_import_path = (find_path / import_path).resolve()
    if absolute_import_path.exists() and absolute_import_path.is_dir():
        for _suffix in include_suffixes:

            dunder_init_file = absolute_import_path / ('__init__' + _suffix)
            if dunder_init_file.exists() and dunder_init_file.is_file():
                return dunder_init_file

    # imported is file module
    for _suffix in include_suffixes:
        absolute_import_path = (find_path / (import_path + _suffix)).resolve()

        if absolute_import_path.exists() and absolute_import_path.is_file():
            return absolute_import_path

    return None


def _resolve_import_node(
    ast_node: Union[builtin_ast.Import, builtin_ast.ImportFrom], 
    module_path: Path,  # the module from which the ast node is produced
    find_path: Path, 
    include_suffixes: Tuple[str, ...] = ('.py', '.pyi')  # TODO: replace to ('.phy', ) when release
) -> List[Path]:
    """ Resolve import ast node into path list of python module or package. """
    imports_path_list: List[Path] = []

    # `Import` ast node
    if isinstance(ast_node, builtin_ast.Import):
        # 'import' ','.dotted_as_name+ 
        for dotted_as_name in ast_node.names:
            # dotted_name: dotted_name '.' NAME | NAME
            dotted_name = dotted_as_name.name
            import_path = _resolve_import_name(
                dotted_name,
                find_path=find_path,
                include_suffixes=include_suffixes
            )

            if import_path is not None:
                imports_path_list.append(import_path)

    # `ImportFrom` ast node
    elif isinstance(ast_node, builtin_ast.ImportFrom):
        # | 'from' ('.' | '...')* dotted_name 'import' import_from_targets 
        # | 'from' ('.' | '...')+ 'import' import_from_targets 
        from_level = ast_node.level

        # level = 0: 'from' dotted_name 'import' import_from_targets 
        if not from_level:
            import_path = _resolve_import_name(
                ast_node.module,
                find_path=find_path,
                include_suffixes=include_suffixes
            )

            if import_path is not None:
                imports_path_list.append(import_path)

        # level > 0
        else:
            module_find_path = module_path
            while from_level:
                module_find_path = module_find_path.parent
                from_level -= 1

            # `ast_node.module is None` means case of `from .|.. import`
            if ast_node.module is None:
                import_path = None

                for _suffix in include_suffixes:
                    dunder_init_file = module_find_path / ('__init__' + _suffix)
                    if dunder_init_file.exists() and dunder_init_file.is_file():
                        import_path = dunder_init_file.resolve()
                        break
                
            else:
                import_path = _resolve_import_name(
                    ast_node.module,
                    find_path=module_find_path,
                    include_suffixes=include_suffixes
                )

            if import_path is not None:
                imports_path_list.append(import_path)
            
    return imports_path_list


def resolve_entry_file(entry_file: Path, find_path: Path = None) -> ImportPathNode:
    """ resolve dependent code files starting from given entry code file """
    entry_file = entry_file.resolve()
    if not (entry_file.exists() and entry_file.is_file()):
        raise FileNotFoundError(str(entry_file))
    
    resolved_files: Set[Path] = set()

    def _resolve_file(_file: Path, find_path=find_path) -> Optional[ImportPathNode]:
        _file = _file.resolve()
        if not _file.exists():
            return None
        
        if find_path is None:
            find_path = Path.cwd()
        find_path = find_path.resolve()
        
        # skip resolved files
        if _file in resolved_files:
            return None
        
        resolved_files.add(_file)

        # resolve import path, recursively
        _import_path_tree: ImportPathNode = {
            'path': str(_file),
            'imports': []
        }

        import_ast_nodes = extract_import_ast_nodes(_file)
        
        for _ast_node in import_ast_nodes:
            resolved_imports_path_list = _resolve_import_node(
                _ast_node, 
                _file, 
                find_path
            )

            # resolve recursively
            for resolved_path in resolved_imports_path_list:
                if _import_path_node := _resolve_file(resolved_path, find_path=find_path):
                    _import_path_tree['imports'].append(_import_path_node)

        return _import_path_tree

    # start recursion
    return _resolve_file(entry_file)


def resolve_entry_package(entry_package: Path, find_path: Path = None) -> ImportPathNode:
    """ regard the `__init__.py` of the entry package as entry file """
    entry_file = (entry_package / '__init__.py').resolve()
    return resolve_entry_file(entry_file, find_path=find_path)
