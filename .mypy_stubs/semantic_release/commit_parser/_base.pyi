import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from git.objects.commit import Commit as Commit
from semantic_release.commit_parser.token import ParseResultType as ParseResultType
from typing import Any, Generic, TypeVar
from semantic_release.commit_parser.token import ParseResultType

class ParserOptions(dict[Any, Any]):
    def __init__(self, **_: Any) -> None: ...

_TT = TypeVar("_TT", bound=ParseResultType)
_OPTS = TypeVar("_OPTS", bound=ParserOptions)

class CommitParser(ABC, Generic[_TT, _OPTS], metaclass=abc.ABCMeta):
    parser_options: type[_OPTS]
    options: Incomplete
    def __init__(self, options: _OPTS) -> None: ...
    @abstractmethod
    def parse(self, commit: Commit) -> _TT: ...
