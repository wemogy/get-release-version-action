from _typeshed import Incomplete
from semantic_release.cli.commands.cli_context import CliContextObj as CliContextObj
from semantic_release.cli.util import noop_report as noop_report
from semantic_release.version import tags_and_versions as tags_and_versions

log: Incomplete

def publish(cli_ctx: CliContextObj, tag: str = 'latest') -> None: ...
