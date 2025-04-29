""" resolve import node to module or package path """
# imports
import ast as builtin_ast
from pathlib import Path
from typing import Tuple, Optional, Union


def resolve_import_node(
        ast_node: Union[builtin_ast.Import, builtin_ast.ImportFrom], 
        base_path: Path, 
        include_suffixes: Tuple[str, ...] = ('.py', '.pyi')
    ) -> Optional[Path]:
    """ resolve import name into path of python module or package """
    for _suffix in include_suffixes:
        mod_path = name.replace('.', os.sep) + _suffix
        abs_path = (base_path / mod_path).resolve()

        if abs_path.exists():
            return abs_path

    return None
