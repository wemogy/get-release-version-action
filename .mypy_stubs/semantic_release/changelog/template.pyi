import os
from _typeshed import Incomplete
from jinja2 import Environment as Environment
from jinja2.sandbox import SandboxedEnvironment
from pathlib import Path
from semantic_release.helpers import dynamic_import as dynamic_import
from typing import Iterable, Literal

log: Incomplete

def environment(template_dir: Path | str = '.', block_start_string: str = '{%', block_end_string: str = '%}', variable_start_string: str = '{{', variable_end_string: str = '}}', comment_start_string: str = '{#', comment_end_string: str = '#}', line_statement_prefix: str | None = None, line_comment_prefix: str | None = None, trim_blocks: bool = False, lstrip_blocks: bool = False, newline_sequence: Literal['\n', '\r', '\r\n'] = '\n', keep_trailing_newline: bool = False, extensions: Iterable[str] = (), autoescape: bool | str = True) -> SandboxedEnvironment: ...
def recursive_render(template_dir: Path, environment: Environment, _root_dir: str | os.PathLike[str] = '.') -> list[str]: ...
