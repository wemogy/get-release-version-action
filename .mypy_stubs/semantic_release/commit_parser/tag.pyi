from _typeshed import Incomplete
from git.objects.commit import Commit as Commit
from semantic_release.commit_parser._base import CommitParser as CommitParser, ParserOptions as ParserOptions
from semantic_release.commit_parser.token import ParseError as ParseError, ParseResult as ParseResult, ParsedCommit as ParsedCommit
from semantic_release.commit_parser.util import breaking_re as breaking_re, parse_paragraphs as parse_paragraphs
from semantic_release.enums import LevelBump as LevelBump

log: Incomplete
re_parser: Incomplete

class TagParserOptions(ParserOptions):
    minor_tag: str
    patch_tag: str

class TagCommitParser(CommitParser[ParseResult, TagParserOptions]):
    parser_options = TagParserOptions
    def parse(self, commit: Commit) -> ParseResult: ...
