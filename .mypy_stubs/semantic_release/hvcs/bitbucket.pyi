from _typeshed import Incomplete
from semantic_release.hvcs._base import HvcsBase as HvcsBase
from semantic_release.hvcs.token_auth import TokenAuth as TokenAuth
from semantic_release.hvcs.util import build_requests_session as build_requests_session

log: Incomplete

class Bitbucket(HvcsBase):
    API_VERSION: str
    DEFAULT_DOMAIN: str
    DEFAULT_API_DOMAIN: str
    DEFAULT_ENV_TOKEN_NAME: str
    hvcs_domain: Incomplete
    hvcs_api_domain: Incomplete
    api_url: Incomplete
    token: Incomplete
    session: Incomplete
    def __init__(self, remote_url: str, hvcs_domain: str | None = None, hvcs_api_domain: str | None = None, token: str | None = None) -> None: ...
    def compare_url(self, from_rev: str, to_rev: str) -> str: ...
    def remote_url(self, use_token: bool = True) -> str: ...
    def commit_hash_url(self, commit_hash: str) -> str: ...
    def pull_request_url(self, pr_number: str | int) -> str: ...
