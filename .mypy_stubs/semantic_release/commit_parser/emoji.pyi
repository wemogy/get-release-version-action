from _typeshed import Incomplete
from git.objects.commit import Commit as Commit
from semantic_release.commit_parser._base import CommitParser as CommitParser, ParserOptions as ParserOptions
from semantic_release.commit_parser.token import ParseResult as ParseResult, ParsedCommit as ParsedCommit
from semantic_release.commit_parser.util import parse_paragraphs as parse_paragraphs
from semantic_release.enums import LevelBump as LevelBump
from typing import Tuple

logger: Incomplete

class EmojiParserOptions(ParserOptions):
    major_tags: Tuple[str, ...]
    minor_tags: Tuple[str, ...]
    patch_tags: Tuple[str, ...]
    default_bump_level: LevelBump

class EmojiCommitParser(CommitParser[ParseResult, EmojiParserOptions]):
    parser_options = EmojiParserOptions
    def parse(self, commit: Commit) -> ParseResult: ...
