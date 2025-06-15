""" cli """
# imports
from pathlib import Path
import json

import click

# local imports
from phy_imports_resolver import ImportResolver


@click.group()
def phy():
    """ resolve imports """
    pass


@phy.command()
@click.option('-f', '--file', type=click.Path(exists=True), help='Path to the entry code file')
def resolve_imports(file: Path):
    """ resolve imports from entry code file """
    project_dir = Path.cwd().resolve()
    resolver = ImportResolver(project_dir=project_dir)

    entry_file_path = Path(file).resolve()
    resolved_result = resolver.start(entry_file_path)
    click.echo(str(resolved_result))


if __name__ == '__main__':
    phy()
