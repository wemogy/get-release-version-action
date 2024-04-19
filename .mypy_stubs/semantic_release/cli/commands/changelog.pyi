from _typeshed import Incomplete
from semantic_release.changelog import ReleaseHistory as ReleaseHistory, recursive_render as recursive_render
from semantic_release.changelog.context import make_changelog_context as make_changelog_context
from semantic_release.cli.commands.cli_context import CliContextObj as CliContextObj
from semantic_release.cli.common import get_release_notes_template as get_release_notes_template, render_default_changelog_file as render_default_changelog_file, render_release_notes as render_release_notes
from semantic_release.cli.util import noop_report as noop_report
from semantic_release.version import Version as Version

log: Incomplete

def changelog(cli_ctx: CliContextObj, release_tag: str | None = None) -> None: ...
