"""Console script for server_double."""
import cmd
import sys
import time

import click
import yaml

from server_double.server import MockServer


class ServerDoubleShell(cmd.Cmd):
    """
    Interactive shell for Server Double.
    Features a command loop to let you start/stop the server and configure/alter the endpoints.
    """

    intro = "You are now in an interactive shell. Use the 'start' command to start your server double!"
    prompt = "(server double) "

    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.server = None

    def do_start(self, arg):  # pylint: disable=unused-argument
        """Start the server."""
        self.server = MockServer(self.config)
        self.server.start()
        time.sleep(2)
        print("Server double started")

    def do_stop(self, arg):  # pylint: disable=unused-argument
        """Stop the server (if already running)."""
        self.server.stop()
        self.server = None

    def do_quit(self, arg):  # pylint: disable=unused-argument
        """Exit the interactive shell."""
        if self.server:
            self.do_stop(None)
        sys.exit(0)

    def emptyline(self):
        """
        Override of the Cmd implementation to ensure that when hitting enter on an empty prompt no command
        gets executed. The default implementation always repeats the last entered command.
        """
        return None


@click.command()
@click.option("--configfile", default=None, help="YAML configuration file")
def main(configfile):
    """Console script for server_double."""
    click.echo("Starting server double...")
    config = None
    if configfile:
        click.echo("Using config {}".format(configfile))
        with open(configfile) as infile:
            config = yaml.load(infile, yaml.Loader)
    else:
        click.echo("Using default config")
    ServerDoubleShell(config).cmdloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pylint: disable=no-value-for-parameter; # pragma: no cover
