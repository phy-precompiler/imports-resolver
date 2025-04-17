""" cli """
# imports
from pathlib import Path
import json

import click

# local imports
from ._core import resolve_entry_file


@click.group()
def cli():
    """ resolve imports """
    pass


@cli.command()
@click.option('-f', '--file', type=click.Path(exists=True), help='Path to the entry code file')
def cli_resolve_entry_file(file: Path):
    """ resolve imports from entry code file """
    resolved_result = resolve_entry_file(file.resolve())
    click.echo(json.dumps(resolved_result, indent=4))


if __name__ == '__main__':
    cli()
