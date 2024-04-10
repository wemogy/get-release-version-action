from _typeshed import Incomplete
from git.objects.commit import Commit as Commit
from semantic_release.commit_parser._base import CommitParser as CommitParser, ParserOptions as ParserOptions
from semantic_release.commit_parser.token import ParseError as ParseError, ParseResult as ParseResult, ParsedCommit as ParsedCommit
from semantic_release.commit_parser.util import breaking_re as breaking_re, parse_paragraphs as parse_paragraphs
from semantic_release.enums import LevelBump as LevelBump
from typing import Tuple

log: Incomplete
LONG_TYPE_NAMES: Incomplete

class AngularParserOptions(ParserOptions):
    allowed_tags: Tuple[str, ...]
    minor_tags: Tuple[str, ...]
    patch_tags: Tuple[str, ...]
    default_bump_level: LevelBump

class AngularCommitParser(CommitParser[ParseResult, AngularParserOptions]):
    parser_options = AngularParserOptions
    re_parser: Incomplete
    def __init__(self, options: AngularParserOptions) -> None: ...
    def parse(self, commit: Commit) -> ParseResult: ...
