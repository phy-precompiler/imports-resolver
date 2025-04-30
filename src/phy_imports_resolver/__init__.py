""" Resolve imports of a python file or module, exclude site 
packages & builtin modules. 
"""
__version__ = "0.1.0"
__all__ = [
    'resolve_entry_file',
    'resolve_entry_package',
]


# imports
from ._resolve_import import resolve_entry_file, resolve_entry_package
