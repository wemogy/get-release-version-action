"""Shared pytest fixtures for the end-to-end tests."""

from collections.abc import Generator
from pathlib import Path

import pytest
from test_utils import TestRepo, setup_logging


@pytest.fixture(scope='module', autouse=True)
def _setup_logging() -> None:
    """Set up logging for the tests."""
    setup_logging()


@pytest.fixture
def repo(tmp_path: Path) -> Generator[TestRepo]:
    """Create a new test git repository."""
    with TestRepo(tmp_path) as test_repo:
        yield test_repo
