"""Wrapper around the git.Repo class that implements concrete methods for unit testing."""
import logging
import os
import shutil
from enum import StrEnum
from pathlib import Path
from tempfile import mkdtemp
from uuid import uuid4

from git import Commit, Repo

logger = logging.getLogger('wemogy.get-release-version-action.tests.repo')


class GitBranchNotFoundError(Exception):
    """Exception for when a git branch is not found."""


class CommitMessages(StrEnum):
    """Pre-made commit messages for conventional commits."""
    CHORE = 'chore: test'
    FIX = 'fix: test'
    FEATURE = 'feat: test'
    BREAKING_FIX = 'fix!: test'
    BREAKING_FEATURE = 'feat!: test'


class TestRepo:
    """Wrapper around the git.Repo class that implements concrete methods for unit testing."""
    path: Path
    repo: Repo
    keep_repository_dir: bool

    def __init__(self, keep_repository_dir: bool = False) -> None:
        """Wrapper around the git.Repo class that implements concrete methods for unit testing."""
        self.keep_repository_dir = keep_repository_dir
        self.path = Path(mkdtemp(prefix='wemogy.get-release-version-action.tests'))
        logger.info('Created git repository in directory %s', self.path)
        os.chdir(self.path)

        # Initialize repository and make initial commit
        self.repo = Repo.init(self.path, initial_branch='main')
        self.commit('Initial commit', 'README.md')

        # Set up branches: release, release-beta, release-prod
        self.create_branch('release', 'main')
        self.create_branch('release-beta', 'release')
        self.create_branch('release-prod', 'release-beta')
        self.checkout('main')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        """Remove the test repo."""
        self.repo.close()

        if not self.keep_repository_dir:
            logger.info('Removing repository %s', self.path)
            shutil.rmtree(self.path)
        else:
            logger.info('Keeping repository %s', self.path)

    def create_branch(self, name: str, base_name: str | None) -> None:
        """Create a branch named `name` that is based on the branch with `base_name` and check it out."""
        if base_name is not None:
            self.checkout(base_name)
        self.repo.create_head(name)
        self.checkout(name)

    def checkout(self, branch_name: str) -> None:
        """
        Checkout the branch with the specified name.

        :raises GitBranchNotFoundError: If the branch was not found.
        """
        try:
            self.repo.heads[branch_name].checkout()
        except IndexError as exc:
            raise GitBranchNotFoundError(f'Branch {branch_name} was not found') from exc

    def commit(self, commit_message: CommitMessages | str, file_name: str | None = None) -> Commit:
        """
        Create a file and make a commit with the given level as commit message.

        :param commit_message: A conventional commit message.
        :param file_name: An optional file name, if None a random file name is chosen.
        :returns: The created commit.
        """
        file_name = file_name or f'file_{uuid4()}'
        file_path = self.path / file_name
        file_path.write_text('test')

        self.repo.index.add(file_name)
        return self.repo.index.commit(commit_message)

    def merge(self, source_branch_name: str, dest_branch_name: str) -> None:
        """
        Merge a branch into another branch and check out the destination branch.

        :param source_branch_name: The branch name to merge from.
        :param dest_branch_name: The branch name to merge into.
        :raises GitBranchNotFoundError: If the branch was not found.
        """
        self.checkout(dest_branch_name)
        self.repo.git.merge(source_branch_name)

    def cherrypick(self, commit: Commit, dest_branch_name: str) -> None:
        """
        Cherrypick a commit into a branch and check out the destination branch.

        :param commit: The commit to cherrypick.
        :param dest_branch_name: The branch name to cherrypick onto.
        :raises GitBranchNotFoundError: If the branch was not found.
        """
        self.checkout(dest_branch_name)
        self.repo.git.cherry_pick(commit.hexsha)


__all__ = [
    TestRepo,
    CommitMessages,
    GitBranchNotFoundError
]
