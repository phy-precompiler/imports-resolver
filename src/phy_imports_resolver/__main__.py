""" cli """
# imports
from pathlib import Path
import json

import click

# local imports
from .core import resolve_entry_file


@click.group()
def phy():
    """ resolve imports """
    pass


@phy.command()
@click.option('-f', '--file', type=click.Path(exists=True), help='Path to the entry code file')
def resolve_imports(file: Path):
    """ resolve imports from entry code file """
    entry_file_path = Path(file).resolve()
    resolved_result = resolve_entry_file(entry_file_path)
    click.echo(json.dumps(resolved_result, indent=4))


if __name__ == '__main__':
    phy()
