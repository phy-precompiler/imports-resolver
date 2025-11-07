""" cli app by `click` """
# imports
from pathlib import Path
import click

# local imports
from phy_imports_resolver import ImportResolver


@click.group(name='phy-resolve-imports')
def cli_app():
    """ Resolve the imports of a python file or module, recursively. """
    pass


@cli_app.command()
@click.argument(
    'file', 
    type=click.Path(exists=True)
)
def resolve_imports(file: Path):
    """ Resolve imports from entry code file. 
    
    FILE: path to the entry code file.
    """
    project_dir = Path.cwd().resolve()
    resolver = ImportResolver(project_dir=project_dir)

    entry_file_path = Path(file).resolve()
    resolved_result = resolver.start(entry_file_path)
    click.echo(str(resolved_result))


def main():
    """ expose method entry to `pyproject.toml` script spec """
    cli_app()
