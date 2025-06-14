""" resolve import relationship among modules """
# imports
import os
import ast as builtin_ast
from pathlib import Path
from typing import Optional, List

# local imports
from phy_imports_resolver.types import SEARCH_FOR_SUFFIXES, Module, ModuleFile, ModulePackage, \
    ModuleImportsNode, FileModuleImportsNode, PackageModuleImportsNode


class ImportResolver:
    """ resolve importing chain from given entry code file, searching within given project path """

    # instance attributes
    project_dir: Path

    def __init__(self, project_dir: Path = None):
        """ Init resolver with project directory. 
        
        Project is the directory that look for python modules, it is usually the current work directory. 
        """
        if project_dir is None:
            project_dir = Path.cwd()

        # validate
        project_dir = project_dir.resolve()
        if not (project_dir.exists() and project_dir.is_dir()):
            raise FileNotFoundError(str(project_dir))

        self.project_dir = project_dir

    def start(self, entry_file: Path) -> FileModuleImportsNode:
        """ entry file to start resolving """
        mod_file = ModuleFile.create_or_err(name=entry_file.stem, path=entry_file)
        return self._resolve_mod_file(mod_file)

    def _resolve_mod(self, mod: Module) -> Optional[ModuleImportsNode]:
        """ resolve imports of specified module """
        if isinstance(mod, ModuleFile):
            return self._resolve_mod_file(mod)
        elif isinstance(mod, ModulePackage):
            return self._resolve_mod_package(mod)
        else:
            raise TypeError  # never throws

    def _resolve_mod_file(self, mod_file: ModuleFile) -> Optional[FileModuleImportsNode]:
        """ resolve imports of specified module of file """
        for _import_union_ast in mod_file.extract_import_ast():
            if isinstance(_import_union_ast, builtin_ast.Import):
                pass

            elif isinstance(_import_union_ast, builtin_ast.ImportFrom):
                pass

            else:
                raise TypeError  # never occurs
    
    def _resolve_mod_package(self, mod_pkg: ModulePackage) -> Optional[PackageModuleImportsNode]:
        """ Resolve imports of specified module of package. 
        
        The imports of package module is considered as those of its dunder init file. If the package is native namespace 
        package, it is the submodule that should not be resolved instead of the super package.
        """
        if mod_file := mod_pkg.dunder_init_path:
            return PackageModuleImportsNode(
                mod=mod_pkg,
                project_dir=self.project_dir,
                imports=self._resolve_mod_file(mod_file)
            )
        else:
            raise FileNotFoundError(str(mod_pkg.path / '__init__.*'))
    
            
    def _resolve_import_ast(self, import_ast: builtin_ast.Import, mod_file: ModuleFile) -> Optional[FileModuleImportsNode]:
        """ 'import' ','.dotted_as_name+ """
        mod_imports_node_list: List[ModuleImportsNode] = []

        # "import . <as ...>" & "import .<submod> <as...>" are illegal syntax, so in this case no need to care about
        # resolve dot operator.
        for import_name_ast in import_ast.names:
            # dotted_name: dotted_name '.' NAME | NAME
            import_name = import_name_ast.name

            if mod_imports_node := self._resolve_import_name(import_name):
                mod_imports_node_list.append(mod_imports_node)

        return FileModuleImportsNode(mod=mod_file, project_dir=self.project_dir, imports=mod_imports_node_list)
    
    def _resolve_import_from_ast(self, import_from_ast: builtin_ast.ImportFrom, mod_file: ModuleFile) -> Optional[FileModuleImportsNode]:
        """ import_from:
            | 'from' ('.' | '...')* dotted_name 'import' import_from_targets 
            | 'from' ('.' | '...')+ 'import' import_from_targets 
        """
        from_level = import_from_ast.level

        # level = 0: 'from' dotted_name 'import' import_from_targets
        # No dot operator to resolve.
        if not from_level:
            if mod_imports_node := self._resolve_import_name(import_from_ast.module):
                return mod_imports_node

        # level > 0
        else:
            mod_path = mod_file.path
            while from_level:
                mod_path = mod_path.parent
                from_level -= 1

            # `<ast.ImportForm>.module is None` means `from .|.. import`, not `from .|..<submod> import`
            if import_from_ast.module:
                mod_path = mod_path / import_from_ast.module

            # imported is package
            abs_import_path = mod_path.resolve()
            import_name = abs_import_path.stem

            if mod_package := ModulePackage.create_or_null(name=import_name, path=abs_import_path):
                return self._resolve_mod_package(mod_package)
            
            # imported is file
            for _suffix in SEARCH_FOR_SUFFIXES:
                abs_import_path = abs_import_path.with_suffix(_suffix).resolve()
                if mod_file := ModuleFile.create_or_null(name=import_name, path=abs_import_path):
                    return self._resolve_mod_file(mod_file)
                
        return None
    
    def _resolve_import_name(self, import_name: str) -> Optional[ModuleImportsNode]:
        """ Resolve import name for path of file module or package. 

        Import name should be absolute, no relative symbol '.' or '..' is allowed.
        """
        # assert relative import name has been resolved
        assert not import_name.startswith('.')

        # dotted_name '.' NAME | NAME
        import_path = import_name.replace('.', os.sep)

        # imported is package
        abs_import_path = (self.project_dir / import_path).resolve()
        import_name = abs_import_path.stem

        if mod_package := ModulePackage.create_or_null(name=import_name, path=abs_import_path):
            return self._resolve_mod_package(mod_package)
        
        # imported is file
        for _suffix in SEARCH_FOR_SUFFIXES:
            abs_import_path = abs_import_path.with_suffix(_suffix).resolve()
            if mod_file := ModuleFile.create_or_null(name=import_name, path=abs_import_path):
                return self._resolve_mod_file(mod_file)

        # builtin module or site-packages
        return None
