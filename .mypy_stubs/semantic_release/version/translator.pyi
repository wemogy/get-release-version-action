from _typeshed import Incomplete
from semantic_release.const import SEMVER_REGEX as SEMVER_REGEX
from semantic_release.helpers import check_tag_format as check_tag_format
from semantic_release.version.version import Version as Version

log: Incomplete

class VersionTranslator:
    tag_format: Incomplete
    prerelease_token: Incomplete
    from_tag_re: Incomplete
    def __init__(self, tag_format: str = 'v{version}', prerelease_token: str = 'rc') -> None: ...
    def from_string(self, version_str: str) -> Version: ...
    def from_tag(self, tag: str) -> Version | None: ...
    def str_to_tag(self, version_str: str) -> str: ...
