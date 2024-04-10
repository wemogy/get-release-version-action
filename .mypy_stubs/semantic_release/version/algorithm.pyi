from _typeshed import Incomplete
from git.objects.blob import Blob as Blob
from git.objects.commit import Commit as Commit
from git.objects.tag import TagObject as TagObject
from git.objects.tree import Tree as Tree
from git.refs.tag import Tag as Tag
from git.repo.base import Repo as Repo
from semantic_release.commit_parser import CommitParser as CommitParser, ParseResult as ParseResult, ParsedCommit as ParsedCommit, ParserOptions as ParserOptions
from semantic_release.const import DEFAULT_VERSION as DEFAULT_VERSION
from semantic_release.enums import LevelBump as LevelBump
from semantic_release.errors import InvalidVersion as InvalidVersion, MissingMergeBaseError as MissingMergeBaseError
from semantic_release.version.translator import VersionTranslator as VersionTranslator
from semantic_release.version.version import Version as Version
from typing import Iterable

log: Incomplete

def tags_and_versions(tags: Iterable[Tag], translator: VersionTranslator) -> list[tuple[Tag, Version]]: ...
def next_version(repo: Repo, translator: VersionTranslator, commit_parser: CommitParser[ParseResult, ParserOptions], prerelease: bool = False, major_on_zero: bool = True, allow_zero_version: bool = True) -> Version: ...
