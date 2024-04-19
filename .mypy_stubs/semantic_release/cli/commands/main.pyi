import click
from semantic_release.cli.commands.cli_context import CliContextObj as CliContextObj
from semantic_release.cli.config import GlobalCommandLineOptions as GlobalCommandLineOptions
from semantic_release.cli.const import DEFAULT_CONFIG_FILE as DEFAULT_CONFIG_FILE
from semantic_release.cli.util import rprint as rprint

FORMAT: str

def main(ctx: click.Context, config_file: str = ..., verbosity: int = 0, noop: bool = False, strict: bool = False) -> None: ...
