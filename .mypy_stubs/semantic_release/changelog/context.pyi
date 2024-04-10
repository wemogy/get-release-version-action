from dataclasses import dataclass
from jinja2 import Environment as Environment
from semantic_release.changelog.release_history import ReleaseHistory as ReleaseHistory
from semantic_release.hvcs._base import HvcsBase as HvcsBase
from typing import Any, Callable

@dataclass
class ChangelogContext:
    repo_name: str
    repo_owner: str
    history: ReleaseHistory
    filters: tuple[Callable[..., Any], ...] = ...
    def bind_to_environment(self, env: Environment) -> Environment: ...
    def __init__(self, repo_name, repo_owner, history, filters) -> None: ...

def make_changelog_context(hvcs_client: HvcsBase, release_history: ReleaseHistory) -> ChangelogContext: ...
