import click
import logging
from _typeshed import Incomplete
from semantic_release.cli.config import GlobalCommandLineOptions as GlobalCommandLineOptions, RawConfig as RawConfig, RuntimeContext as RuntimeContext
from semantic_release.cli.util import load_raw_config_file as load_raw_config_file, rprint as rprint
from semantic_release.errors import InvalidConfiguration as InvalidConfiguration, NotAReleaseBranch as NotAReleaseBranch

class CliContext(click.Context):
    obj: CliContextObj

class CliContextObj:
    ctx: Incomplete
    logger: Incomplete
    global_opts: Incomplete
    def __init__(self, ctx: click.Context, logger: logging.Logger, global_opts: GlobalCommandLineOptions) -> None: ...
    @property
    def runtime_ctx(self) -> RuntimeContext: ...
