""" cli app by `click` """
# imports
from pathlib import Path
try:
    import click
except ImportError as err:
    raise SystemExit(
        'The CLI requires extra dependencies. ' +
        'Please install with `pip install phy-imports-resolver[cli]`.'
    ) from err

# local imports
from phy_imports_resolver import ImportResolver


@click.command(name='resolve-imports')
@click.argument(
    'file', 
    type=click.Path(exists=True)
)
def cli_app(file: Path):
    """ Resolve the imports of a python file or module, recursively.
    
    FILE: path to the entry code file.
    """
    project_dir = Path.cwd().resolve()
    resolver = ImportResolver(project_dir=project_dir)

    entry_file_path = Path(file).resolve()
    resolved_result = resolver.start(entry_file_path)
    click.echo(str(resolved_result))


def main():
    """ expose method entry to `pyproject.toml` script spec """
    # this is click command; pylint: disable=no-value-for-parameter
    cli_app()
