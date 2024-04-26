from semantic_release.commit_parser import CommitParser as CommitParser, ParseError as ParseError, ParseResult as ParseResult, ParseResultType as ParseResultType, ParsedCommit as ParsedCommit, ParserOptions as ParserOptions
from semantic_release.enums import LevelBump as LevelBump
from semantic_release.errors import CommitParseError as CommitParseError, InvalidConfiguration as InvalidConfiguration, InvalidVersion as InvalidVersion, SemanticReleaseBaseError as SemanticReleaseBaseError
from semantic_release.version import Version as Version, VersionTranslator as VersionTranslator, next_version as next_version, tags_and_versions as tags_and_versions

__version__: str

def setup_hook(argv: list[str]) -> None: ...
