import subprocess
from _typeshed import Incomplete
from git import Repo as Repo
from git.refs.tag import Tag as Tag
from semantic_release.changelog import ReleaseHistory as ReleaseHistory, environment as environment, recursive_render as recursive_render
from semantic_release.changelog.context import make_changelog_context as make_changelog_context
from semantic_release.cli.commands.cli_context import CliContextObj as CliContextObj
from semantic_release.cli.common import get_release_notes_template as get_release_notes_template, render_default_changelog_file as render_default_changelog_file, render_release_notes as render_release_notes
from semantic_release.cli.github_actions_output import VersionGitHubActionsOutput as VersionGitHubActionsOutput
from semantic_release.cli.util import indented as indented, noop_report as noop_report, rprint as rprint
from semantic_release.const import DEFAULT_SHELL as DEFAULT_SHELL, DEFAULT_VERSION as DEFAULT_VERSION
from semantic_release.enums import LevelBump as LevelBump
from semantic_release.version import Version as Version, VersionTranslator as VersionTranslator, next_version as next_version, tags_and_versions as tags_and_versions
from semantic_release.version.declaration import VersionDeclarationABC as VersionDeclarationABC
from typing import Iterable

log: Incomplete

def is_forced_prerelease(force_prerelease: bool, force_level: str | None, prerelease: bool) -> bool: ...
def last_released(repo: Repo, translator: VersionTranslator) -> tuple[Tag, Version] | None: ...
def version_from_forced_level(repo: Repo, level_bump: LevelBump, translator: VersionTranslator) -> Version: ...
def apply_version_to_source_files(repo: Repo, version_declarations: Iterable[VersionDeclarationABC], version: Version, noop: bool = False) -> list[str]: ...
def shell(cmd: str, *, check: bool = True) -> subprocess.CompletedProcess: ...
def version(cli_ctx: CliContextObj, print_only: bool = False, print_only_tag: bool = False, print_last_released: bool = False, print_last_released_tag: bool = False, force_prerelease: bool = False, prerelease_token: str | None = None, force_level: str | None = None, commit_changes: bool = True, create_tag: bool = True, update_changelog: bool = True, push_changes: bool = True, make_vcs_release: bool = True, build_metadata: str | None = None, skip_build: bool = False) -> str: ...
