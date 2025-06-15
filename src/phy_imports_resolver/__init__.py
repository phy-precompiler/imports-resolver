""" Resolve imports of a python file or module, exclude site packages & builtin modules. """
__version__ = "0.2.0"
__all__ = [
    'ImportResolver',
    'SEARCH_FOR_SUFFIXES',
]


# imports
from phy_imports_resolver.resolver import ImportResolver
from phy_imports_resolver.types import SEARCH_FOR_SUFFIXES
