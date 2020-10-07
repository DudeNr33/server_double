"""Console script for server_double."""
import cmd
import sys
import time

import click
import yaml

from server_double.server import MockServer


class ServerDoubleShell(cmd.Cmd):
    intro = "You are now in an interactive shell. Use the 'start' command to start your server double!"
    prompt = "(server double) "

    def __init__(self, config=None):
        super(ServerDoubleShell, self).__init__()
        self.config = config
        self.server = None

    def do_start(self, arg):
        self.server = MockServer(self.config)
        self.server.start()
        time.sleep(2)
        print("Server double started at {}".format(self.server.url))

    def do_stop(self, arg):
        self.server.shutdown_server()
        self.server = None

    def do_quit(self, arg):
        if self.server:
            self.do_stop(None)
        sys.exit(0)

    def emptyline(self):
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
    sys.exit(main())  # pragma: no cover
