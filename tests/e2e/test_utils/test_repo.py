"""Wrapper around the ``git.Repo`` class that implements specific methods for unit testing."""
from __future__ import annotations

import logging
import os
from enum import StrEnum
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from uuid import uuid4

from get_release_version_action.utils.git import tag_creation_history

from git import Commit, Repo

logger = logging.getLogger('wemogy.get-release-version-action.tests.repo')

__all__ = [
    'GitBranchNotFoundError',
    'CommitMessages',
    'TestRepo'
]


class GitBranchNotFoundError(Exception):
    """Raised when a git branch is not found."""


class CommitMessages(StrEnum):
    """Pre-made commit messages for conventional commits."""
    CHORE = 'chore: test'
    FIX = 'fix: test'
    FEATURE = 'feat: test'
    BREAKING_FIX = 'fix!: test'
    BREAKING_FEATURE = 'feat!: test'


class TestRepo:
    """Wrapper around the ``git.Repo`` class that implements specific methods for unit testing."""
    tempdir: TemporaryDirectory
    repo: Repo

    def __init__(self, *, keep_repository_dir: bool = False) -> None:
        """
        Wrapper around the ``git.Repo`` class that implements specific methods for unit testing.

        This creates a new git repo in a temporary directory, makes an initial README commit to the ``main`` branch
        and creates 3 branches called ``release``, ``release-beta`` and ``release-prod``.
        """
        self.tempdir = TemporaryDirectory(
            prefix='wemogy.get-release-version-action.tests',
            ignore_cleanup_errors=True,
            delete=not keep_repository_dir
        )

        logger.info('Creating git repository in directory %s', self.path)
        os.chdir(self.path)

        # Clear tag creation history
        tag_creation_history.clear()

        # Initialize repository and make initial commit.
        self.repo = Repo.init(self.path, initial_branch='main')
        self.commit('Initial commit', 'README.md')

        # Set up branches: release, release-beta, release-prod
        self.create_branch('release', 'main')
        self.create_branch('release-beta', 'release')
        self.create_branch('release-prod', 'release-beta')
        self.checkout('main')

        logger.info('Initializing done')

    def __enter__(self) -> TestRepo:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    @property
    def path(self) -> Path:
        """Get the path of the temporary directory."""
        return Path(self.tempdir.name)

    def close(self) -> None:
        """Close the ``git.Repo`` object."""
        self.repo.close()

    def create_branch(self, name: str, base_name: str | None) -> None:
        """Create a branch named ``name`` that is based on the branch with ``base_name`` and check it out."""
        logger.info('Creating branch %s from %s', name, base_name)

        if base_name is not None:
            self.checkout(base_name)

        self.repo.create_head(name)
        self.checkout(name)

    def checkout(self, branch_name: str) -> None:
        """
        Checkout the branch with the specified name.

        :raises GitBranchNotFoundError: If the branch was not found.
        """
        logger.info('Checking out branch %s', branch_name)

        try:
            self.repo.heads[branch_name].checkout()
        except IndexError as exc:
            raise GitBranchNotFoundError(f'Branch {branch_name} was not found') from exc

    def commit(self, message: CommitMessages | str, file_name: str | None = None) -> Commit:
        """
        Create a file and make a commit with the given level as commit message.

        :param message: A conventional commit message.
        :param file_name: An optional file name. Defaults to ``file_{uuid4()}``.
        :returns: The created commit.
        """
        file_name = file_name or f'file_{uuid4()}'
        file_path = self.path / file_name
        file_path.write_text('test', encoding='utf-8')

        logger.info('Committing file %s with message %s', file_name, message)
        self.repo.index.add(file_name)
        return self.repo.index.commit(message)

    def merge(self, source_branch_name: str, dest_branch_name: str) -> None:
        """
        Merge a branch into another branch and check out the destination branch.

        :param source_branch_name: The branch name to merge from.
        :param dest_branch_name: The branch name to merge into.
        :raises GitBranchNotFoundError: If the destination branch was not found.
        """
        logger.info('Merging branch %s into branch %s', source_branch_name, dest_branch_name)
        self.checkout(dest_branch_name)
        self.repo.git.merge(source_branch_name)

    def cherrypick(self, commit: Commit, dest_branch_name: str) -> None:
        """
        Cherrypick a commit into a branch and check out the destination branch.

        :param commit: The commit to cherrypick.
        :param dest_branch_name: The branch name to cherrypick onto.
        :raises GitBranchNotFoundError: If the branch was not found.
        """
        logger.info('Cherrypicking commit %s (%s) into branch %s',
                    commit.message, commit.hexsha, dest_branch_name)
        self.checkout(dest_branch_name)
        self.repo.git.cherry_pick(commit.hexsha)

    def get_latest_tag_name(self) -> str | None:
        """Return the newest tag name or ``None``, if no tags exist."""
        logger.info(tag_creation_history)

        try:
            return tag_creation_history[-1]
        except IndexError:
            return None
