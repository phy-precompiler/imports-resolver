""" resolve import node to the path of file module or package """
# imports
import os
import ast as builtin_ast
from pathlib import Path
from typing import Tuple, Optional, Union, List, TypedDict


# typings
class ImportPathTree(TypedDict):
    """ json schema for import path tree """
    path: str
    imports: List['ImportPathTree']


def resolve_import_name(
    import_name: str,
    base_path: Path, 
    include_suffixes: Tuple[str, ...] = ('.py', '.pyi')  # TODO: replace to ('.phy', ) when release
) -> Optional[Path]:
    """ Resolve import name into path of python module or package. 

    Only the modules or packages within given `base_base` should be taken into account. Other ones in site-packages, 
    or customized PYTHONPATH, even though can be resolved, cannot or should not be processed by `phy` toolchain.
    """
    # dotted_name '.' NAME | NAME
    import_path = import_name.replace('.', os.sep)

    # imported is package; return __init__ file path
    absolute_import_path = (base_path / import_path).resolve()
    if absolute_import_path.exists() and absolute_import_path.is_dir():
        for _suffix in include_suffixes:

            dunder_init_file = absolute_import_path / ('__init__' + _suffix)
            if dunder_init_file.exists() and dunder_init_file.is_file():
                return dunder_init_file

    # imported is file module
    for _suffix in include_suffixes:
        absolute_import_path = (base_path / (import_path + _suffix)).resolve()

        if absolute_import_path.exists() and absolute_import_path.is_file():
            return absolute_import_path

    return None


def resolve_import_node(
    ast_node: Union[builtin_ast.Import, builtin_ast.ImportFrom], 
    base_path: Path, 
    include_suffixes: Tuple[str, ...] = ('.py', '.pyi')  # TODO: replace to ('.phy', ) when release
) -> Optional[Path]:
    """ Resolve import name into path of python module or package. 

    Only the modules or packages within given `base_base` should be taken into account. Other ones in site-packages, 
    or customized PYTHONPATH, even though can be resolved, cannot or should not be processed by `phy` toolchain.
    """
    imports_path_list: List[Path] = []

    # `Import` ast node
    if isinstance(ast_node, builtin_ast.Import):
        # 'import' ','.dotted_as_name+ 
        for dotted_as_name in ast_node.names:
            # dotted_name '.' NAME | NAME
            dotted_name = dotted_as_name.name

            if not '.' in dotted_name:
                NAME = dotted_name

                for _suffix in include_suffixes:
                    import_path = (base_path / (NAME + _suffix)).resolve()


    return None
