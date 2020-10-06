"""Console script for server_double."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for server_double."""
    click.echo("Replace this message by putting your code into "
               "server_double.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
