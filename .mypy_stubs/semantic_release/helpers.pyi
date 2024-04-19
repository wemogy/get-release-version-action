import logging
from typing import Any, Callable, NamedTuple, TypeVar

log: logging.Logger
_R = TypeVar("_R")
_FuncType = Callable[..., _R]

def format_arg(value: Any) -> str: ...
def check_tag_format(tag_format: str) -> None: ...
def logged_function(logger: logging.Logger) -> Callable[[_FuncType[_R]], _FuncType[_R]]: ...
def dynamic_import(import_path: str) -> Any: ...

class ParsedGitUrl(NamedTuple):
    scheme: str
    netloc: str
    namespace: str
    repo_name: str

def parse_git_url(url: str) -> ParsedGitUrl: ...
