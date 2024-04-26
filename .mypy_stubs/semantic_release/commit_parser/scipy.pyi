from _typeshed import Incomplete
from git.objects.commit import Commit as Commit
from semantic_release.commit_parser._base import CommitParser as CommitParser, ParserOptions as ParserOptions
from semantic_release.commit_parser.token import ParseError as ParseError, ParseResult as ParseResult, ParsedCommit as ParsedCommit
from semantic_release.enums import LevelBump as LevelBump
from typing import Tuple

log: Incomplete
tag_to_section: Incomplete

class ScipyParserOptions(ParserOptions):
    allowed_tags: Tuple[str, ...]
    major_tags: Tuple[str, ...]
    minor_tags: Tuple[str, ...]
    patch_tags: Tuple[str, ...]
    default_level_bump: LevelBump
    tag_to_level: Incomplete
    def __post_init__(self) -> None: ...

class ScipyCommitParser(CommitParser[ParseResult, ScipyParserOptions]):
    parser_options = ScipyParserOptions
    re_parser: Incomplete
    def __init__(self, options: ScipyParserOptions) -> None: ...
    def parse(self, commit: Commit) -> ParseResult: ...
