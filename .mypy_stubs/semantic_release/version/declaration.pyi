import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from pathlib import Path
from semantic_release.version.version import Version as Version
from typing import Any

log: Incomplete

class VersionDeclarationABC(ABC, metaclass=abc.ABCMeta):
    path: Incomplete
    search_text: Incomplete
    def __init__(self, path: Path | str, search_text: str) -> None: ...
    @property
    def content(self) -> str: ...
    @content.setter
    def _(self, _: Any) -> None: ...
    @content.deleter
    def _(self) -> None: ...
    @abstractmethod
    def parse(self) -> set[Version]: ...
    @abstractmethod
    def replace(self, new_version: Version) -> str: ...
    def write(self, content: str) -> None: ...

class TomlVersionDeclaration(VersionDeclarationABC):
    def parse(self) -> set[Version]: ...
    def replace(self, new_version: Version) -> str: ...

class PatternVersionDeclaration(VersionDeclarationABC):
    search_re: Incomplete
    def __init__(self, path: Path | str, search_text: str) -> None: ...
    def parse(self) -> set[Version]: ...
    def replace(self, new_version: Version) -> str: ...