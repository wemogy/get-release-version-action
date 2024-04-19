"""Common fixtures for all tests."""
from collections.abc import Generator
from pathlib import Path

from pytest import fixture

from .logger import setup_logging
from .test_repo import TestRepo

__all__ = [
    'logging',
    'repo'
]


@fixture(scope='module', autouse=True)
def logging() -> None:
    """Setup logging."""
    setup_logging()


@fixture
def repo(tmp_path: Path) -> Generator[TestRepo, None, None]:
    """Create a new test git repository."""
    with TestRepo(tmp_path) as test_repo:
        yield test_repo
