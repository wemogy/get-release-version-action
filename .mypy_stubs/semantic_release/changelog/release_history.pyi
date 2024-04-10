from _typeshed import Incomplete
from datetime import datetime
from git.repo.base import Repo as Repo
from git.util import Actor
from re import Pattern
from semantic_release.commit_parser import CommitParser as CommitParser, ParseError as ParseError, ParseResult as ParseResult, ParserOptions as ParserOptions
from semantic_release.version.algorithm import tags_and_versions as tags_and_versions
from semantic_release.version.translator import VersionTranslator as VersionTranslator
from semantic_release.version.version import Version as Version
from typing import Iterable, Iterator, TypedDict

log: Incomplete

class ReleaseHistory:
    @classmethod
    def from_git_history(cls, repo: Repo, translator: VersionTranslator, commit_parser: CommitParser[ParseResult, ParserOptions], exclude_commit_patterns: Iterable[Pattern[str]] = ()) -> ReleaseHistory: ...
    released: Incomplete
    unreleased: Incomplete
    def __init__(self, unreleased: dict[str, list[ParseResult]], released: dict[Version, Release]) -> None: ...
    def __iter__(self) -> Iterator[dict[str, list[ParseResult]] | dict[Version, Release]]: ...
    def release(self, version: Version, tagger: Actor, committer: Actor, tagged_date: datetime) -> ReleaseHistory: ...

class Release(TypedDict):
    tagger: Actor
    committer: Actor
    tagged_date: datetime
    elements: dict[str, list[ParseResult]]
