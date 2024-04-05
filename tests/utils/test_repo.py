"""Wrapper around the ``git.Repo`` class that implements specific methods for unit testing."""
import logging
import os
import shutil
from enum import StrEnum
from pathlib import Path
from tempfile import mkdtemp
from uuid import uuid4

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
    path: Path
    repo: Repo

    def __init__(self):
        """
        Wrapper around the ``git.Repo`` class that implements specific methods for unit testing.

        This creates a new git repo in a temporary directory, makes an initial README commit to the ``main`` branch
        and creates 3 branches called ``release``, ``release-beta`` and ``release-prod``.
        """
        self.path = Path(mkdtemp(prefix='wemogy.get-release-version-action.tests'))
        logger.info('Creating git repository in directory %s', self.path)
        os.chdir(self.path)

        # Initialize repository and make initial commit.
        self.repo = Repo.init(self.path, initial_branch='main')
        self.commit('Initial commit', 'README.md')

        # Set up branches: release, release-beta, release-prod
        self.create_branch('release', 'main')
        self.create_branch('release-beta', 'release')
        self.create_branch('release-prod', 'release-beta')
        self.checkout('main')

        logger.info('Initializing done')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self, keep_repository_dir: bool = False) -> None:
        """Close the ``git.Repo`` object and delete the temporary folder unless specified otherwise."""
        self.repo.close()

        if not keep_repository_dir:
            logger.info('Removing repository %s', self.path)
            shutil.rmtree(self.path)
        else:
            logger.warning('Keeping repository %s', self.path)

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
        file_path.write_text('test')

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
        try:
            return sorted(self.repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True)[0].name
        except IndexError:
            return None
