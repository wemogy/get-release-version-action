from _typeshed import Incomplete
from semantic_release.helpers import parse_git_url as parse_git_url
from semantic_release.hvcs.token_auth import TokenAuth as TokenAuth
from semantic_release.hvcs.util import build_requests_session as build_requests_session

logger: Incomplete

class HvcsBase:
    DEFAULT_ENV_TOKEN_NAME: str
    hvcs_domain: Incomplete
    hvcs_api_domain: Incomplete
    token: Incomplete
    session: Incomplete
    def __init__(self, remote_url: str, hvcs_domain: str | None = None, hvcs_api_domain: str | None = None, token: str | None = None) -> None: ...
    @property
    def repo_name(self) -> str: ...
    @property
    def owner(self) -> str: ...
    def compare_url(self, from_rev: str, to_rev: str) -> str: ...
    def upload_dists(self, tag: str, dist_glob: str) -> int: ...
    def create_release(self, tag: str, release_notes: str, prerelease: bool = False) -> int | str: ...
    def get_release_id_by_tag(self, tag: str) -> int | None: ...
    def edit_release_notes(self, release_id: int, release_notes: str) -> int: ...
    def create_or_update_release(self, tag: str, release_notes: str, prerelease: bool = False) -> int | str: ...
    def asset_upload_url(self, release_id: str) -> str | None: ...
    def upload_asset(self, release_id: int | str, file: str, label: str | None = None) -> bool: ...
    def remote_url(self, use_token: bool) -> str: ...
    def commit_hash_url(self, commit_hash: str) -> str: ...
    def pull_request_url(self, pr_number: str) -> str: ...
