from _typeshed import Incomplete
from requests import Session
from requests.packages.urllib3.util.retry import Retry
from semantic_release.hvcs.token_auth import TokenAuth as TokenAuth
from typing import Callable

logger: Incomplete

def build_requests_session(raise_for_status: bool = True, retry: bool | int | Retry = True, auth: TokenAuth | None = None) -> Session: ...
def suppress_http_error_for_codes(*codes: int) -> Callable[[Callable[..., _R]], Callable[..., _R | None]]: ...

suppress_not_found: Incomplete
