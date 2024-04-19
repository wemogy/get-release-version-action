from _typeshed import Incomplete
from git.objects.commit import Commit as Commit
from semantic_release.enums import LevelBump as LevelBump
from semantic_release.errors import CommitParseError as CommitParseError
from typing import NamedTuple, NoReturn

class ParsedCommit(NamedTuple):
    bump: LevelBump
    type: str
    scope: str
    descriptions: list[str]
    breaking_descriptions: list[str]
    commit: Commit
    @property
    def message(self) -> str: ...
    @property
    def hexsha(self) -> str: ...
    @property
    def short_hash(self) -> str: ...

class ParseError(NamedTuple):
    commit: Commit
    error: str
    @property
    def message(self) -> str: ...
    @property
    def hexsha(self) -> str: ...
    @property
    def short_hash(self) -> str: ...
    def raise_error(self) -> NoReturn: ...

ParseResultType: Incomplete
ParseResult = ParseResultType[ParsedCommit, ParseError]
