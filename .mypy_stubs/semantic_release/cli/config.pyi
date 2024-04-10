import re
from _typeshed import Incomplete
from dataclasses import dataclass
from enum import Enum
from git import Actor
from git.repo.base import Repo
from jinja2 import Environment as Environment
from pathlib import Path
from pydantic import BaseModel
from semantic_release import hvcs as hvcs
from semantic_release.changelog import environment as environment
from semantic_release.cli.const import DEFAULT_CONFIG_FILE as DEFAULT_CONFIG_FILE
from semantic_release.cli.masking_filter import MaskingFilter as MaskingFilter
from semantic_release.commit_parser import AngularCommitParser as AngularCommitParser, CommitParser as CommitParser, EmojiCommitParser as EmojiCommitParser, ParseResult as ParseResult, ParserOptions as ParserOptions, ScipyCommitParser as ScipyCommitParser, TagCommitParser as TagCommitParser
from semantic_release.const import COMMIT_MESSAGE as COMMIT_MESSAGE, DEFAULT_COMMIT_AUTHOR as DEFAULT_COMMIT_AUTHOR, SEMVER_REGEX as SEMVER_REGEX
from semantic_release.errors import InvalidConfiguration as InvalidConfiguration, NotAReleaseBranch as NotAReleaseBranch
from semantic_release.helpers import dynamic_import as dynamic_import
from semantic_release.version import VersionTranslator as VersionTranslator
from semantic_release.version.declaration import PatternVersionDeclaration as PatternVersionDeclaration, TomlVersionDeclaration as TomlVersionDeclaration, VersionDeclarationABC as VersionDeclarationABC
from typing import Any, Dict, List, Literal, Tuple
from typing_extensions import Self

log: Incomplete
NonEmptyString: Incomplete

class HvcsClient(str, Enum):
    BITBUCKET: str
    GITHUB: str
    GITLAB: str
    GITEA: str

class EnvConfigVar(BaseModel):
    env: str
    default: str | None
    default_env: str | None
    def getvalue(self) -> str | None: ...
MaybeFromEnv = EnvConfigVar | str

class ChangelogEnvironmentConfig(BaseModel):
    block_start_string: str
    block_end_string: str
    variable_start_string: str
    variable_end_string: str
    comment_start_string: str
    comment_end_string: str
    line_statement_prefix: str | None
    line_comment_prefix: str | None
    trim_blocks: bool
    lstrip_blocks: bool
    newline_sequence: Literal['\n', '\r', '\r\n']
    keep_trailing_newline: bool
    extensions: Tuple[str, ...]
    autoescape: bool | str

class ChangelogConfig(BaseModel):
    template_dir: str
    changelog_file: str
    exclude_commit_patterns: Tuple[str, ...]
    environment: ChangelogEnvironmentConfig

class BranchConfig(BaseModel):
    match: str
    prerelease_token: str
    prerelease: bool

class RemoteConfig(BaseModel):
    name: str
    token: MaybeFromEnv
    url: MaybeFromEnv | None
    type: HvcsClient
    domain: str | None
    api_domain: str | None
    ignore_token_for_push: bool
    def set_default_token(self) -> Self: ...

class PublishConfig(BaseModel):
    dist_glob_patterns: Tuple[str, ...]
    upload_to_vcs_release: bool

class RawConfig(BaseModel):
    assets: List[str]
    branches: Dict[str, BranchConfig]
    build_command: str | None
    changelog: ChangelogConfig
    commit_author: MaybeFromEnv
    commit_message: str
    commit_parser: NonEmptyString
    commit_parser_options: Dict[str, Any]
    logging_use_named_masks: bool
    major_on_zero: bool
    allow_zero_version: bool
    remote: RemoteConfig
    tag_format: str
    publish: PublishConfig
    version_toml: Tuple[str, ...] | None
    version_variables: Tuple[str, ...] | None
    def set_default_opts(self) -> Self: ...

@dataclass
class GlobalCommandLineOptions:
    noop: bool = ...
    verbosity: int = ...
    config_file: str = ...
    strict: bool = ...
    def __init__(self, noop, verbosity, config_file, strict) -> None: ...

@dataclass
class RuntimeContext:
    repo: Repo
    commit_parser: CommitParser[ParseResult, ParserOptions]
    version_translator: VersionTranslator
    major_on_zero: bool
    allow_zero_version: bool
    prerelease: bool
    assets: List[str]
    commit_author: Actor
    commit_message: str
    changelog_excluded_commit_patterns: Tuple[re.Pattern[str], ...]
    version_declarations: Tuple[VersionDeclarationABC, ...]
    hvcs_client: hvcs.HvcsBase
    changelog_file: Path
    ignore_token_for_push: bool
    template_environment: Environment
    template_dir: Path
    build_command: str | None
    dist_glob_patterns: Tuple[str, ...]
    upload_to_vcs_release: bool
    global_cli_options: GlobalCommandLineOptions
    masker: MaskingFilter
    @staticmethod
    def resolve_from_env(param: MaybeFromEnv | None) -> str | None: ...
    @staticmethod
    def select_branch_options(choices: Dict[str, BranchConfig], active_branch: str) -> BranchConfig: ...
    def apply_log_masking(self, masker: MaskingFilter) -> MaskingFilter: ...
    @classmethod
    def from_raw_config(cls, raw: RawConfig, global_cli_options: GlobalCommandLineOptions) -> RuntimeContext: ...
    def __init__(self, repo, commit_parser, version_translator, major_on_zero, allow_zero_version, prerelease, assets, commit_author, commit_message, changelog_excluded_commit_patterns, version_declarations, hvcs_client, changelog_file, ignore_token_for_push, template_environment, template_dir, build_command, dist_glob_patterns, upload_to_vcs_release, global_cli_options, masker) -> None: ...
