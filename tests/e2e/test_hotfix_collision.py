"""Test that an already-existing tag does not cause a ``git tag`` collision in suffix-bump mode."""
# pylint: disable=too-many-locals,too-many-statements,duplicate-code,unused-import,redefined-outer-name
from assertpy import assert_that

from test_utils import ActionInputs, CommitMessages, logging, TestRepo, repo, run_action


def _fix_release_inputs() -> ActionInputs:
    return ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )


def _fix_beta_inputs() -> ActionInputs:
    return ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )


def _fix_prod_inputs() -> ActionInputs:
    return ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )


def _hotfix_release_inputs() -> ActionInputs:
    return ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )


def _hotfix_beta_inputs() -> ActionInputs:
    return ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        reference_version_suffix='pre',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )


def _hotfix_prod_inputs() -> ActionInputs:
    return ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        reference_version_suffix='beta',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )


def test_hotfix_skips_already_existing_tag(repo: TestRepo) -> None:
    """
    Regression: when the tag the action would produce already exists (e.g. left over from a reverted deploy),
    the action must bump further instead of failing with ``fatal: tag 'X' already exists``.

    Scenario:

    1. A normal fix flows through release / release-beta / release-prod, producing ``v0.0.1``.
    2. A stale ``v0.0.1-hotfix.2`` tag pre-exists on an older commit (imagine it survived a reverted deploy).
    3. A first normal hotfix cycle creates ``v0.0.1-hotfix.1`` on a newer commit. This tag sorts first in the
       action's commit-date-based lookup, so on the next hotfix the action computes ``v0.0.1-hotfix.2`` as
       the next tag, which collides with the stale tag.
    4. A second hotfix cycle should advance past the collision, producing ``v0.0.1-hotfix.3``.
    """
    # Arrange: normal fix → pre / beta / prod, producing v0.0.1 on release-prod.
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    run_action(_fix_release_inputs())

    repo.merge('release', 'release-beta')
    run_action(_fix_beta_inputs())

    repo.merge('release-beta', 'release-prod')
    run_action(_fix_prod_inputs())

    # Stale tag on the oldest commit, surviving from a prior (reverted) deploy.
    initial_commit = list(repo.repo.iter_commits('main'))[-1]
    repo.repo.create_tag('v0.0.1-hotfix.2', ref=initial_commit, message='Release v0.0.1-hotfix.2')

    # First hotfix cycle → v0.0.1-hotfix.1 on a newer commit (newer than the stale tag target).
    repo.checkout('main')
    hotfix1_commit = repo.commit(CommitMessages.FIX)

    repo.cherrypick(hotfix1_commit, 'release')
    run_action(_hotfix_release_inputs())

    repo.cherrypick(hotfix1_commit, 'release-beta')
    run_action(_hotfix_beta_inputs())

    repo.cherrypick(hotfix1_commit, 'release-prod')
    output_hotfix1_prod = run_action(_hotfix_prod_inputs())
    assert_that(output_hotfix1_prod.version_name).is_equal_to('v0.0.1-hotfix.1')

    # Act: second hotfix cycle; without the collision-avoidance fix, the prod action fails here
    # with ``fatal: tag 'v0.0.1-hotfix.2' already exists``.
    repo.checkout('main')
    hotfix2_commit = repo.commit(CommitMessages.FIX)

    repo.cherrypick(hotfix2_commit, 'release')
    run_action(_hotfix_release_inputs())

    repo.cherrypick(hotfix2_commit, 'release-beta')
    run_action(_hotfix_beta_inputs())

    repo.cherrypick(hotfix2_commit, 'release-prod')
    output_hotfix2_prod = run_action(_hotfix_prod_inputs())

    # Assert: the action bumped past the stale tag.
    assert_that(output_hotfix2_prod.version_name).is_equal_to('v0.0.1-hotfix.3')
    assert_that(repo.get_latest_tag_name()).is_equal_to('v0.0.1-hotfix.3')
