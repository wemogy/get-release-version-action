"""Test that commits from a branch that stayed open across another release are still analysed."""
# pylint: disable=too-many-locals,too-many-statements,duplicate-code,unused-import,redefined-outer-name
from assertpy import assert_that

from test_utils import ActionInputs, ActionOutputs, CommitMessages, logging, TestRepo, repo, run_action


def _release_inputs() -> ActionInputs:
    return ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )


def _beta_inputs() -> ActionInputs:
    return ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )


def _prod_inputs() -> ActionInputs:
    return ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )


def test_breaking_change_older_than_previous_tag(repo: TestRepo) -> None:
    """
    Regression: a ``feat!:`` commit made on a branch that stayed open across another release must still
    be analysed, even though its commit date is older than the tag of that other release.

    Scenario:

    1. Branch ``feature`` off ``main`` and commit ``feat!:`` there.
    2. While ``feature`` is still open, release a ``fix:`` from ``main``, producing ``v0.0.1``.
       Its tag is therefore newer than the breaking commit.
    3. Merge ``feature`` into ``main`` and release again. The breaking commit is in
       ``v0.0.1..HEAD`` by ancestry, so the version must become ``v1.0.0``.
    """
    # Arrange: a breaking change on a branch that is not released yet.
    repo.create_branch('feature', 'main')
    repo.commit(CommitMessages.BREAKING_FEATURE)

    # A fix is released while the feature branch is open, so its tag is newer than the breaking commit.
    repo.checkout('main')
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    run_action(_release_inputs())

    repo.merge('release', 'release-beta')
    run_action(_beta_inputs())

    repo.merge('release-beta', 'release-prod')
    output_fix_prod = run_action(_prod_inputs())
    assert_that(output_fix_prod.version_name).is_equal_to('v0.0.1')

    # Act: the feature branch lands and gets released.
    repo.merge('feature', 'main')

    repo.merge('main', 'release')
    actual_output_release = run_action(_release_inputs())
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(_beta_inputs())
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(_prod_inputs())
    tag_prod = repo.get_latest_tag_name()

    # Assert: the breaking change is picked up, so the major version is bumped.
    # Without the ancestry-based commit range, the walk stops at the v0.0.1-pre commit and the
    # version stays at 0.0.1.
    assert_that(actual_output_release).is_equal_to(ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='0.0.1-pre',
        previous_version_name='v0.0.1-pre',
        tag_created=True
    ))
    assert_that(tag_release).is_equal_to('v1.0.0-pre')

    assert_that(actual_output_beta).is_equal_to(ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='0.0.1-beta',
        previous_version_name='v0.0.1-beta',
        tag_created=True
    ))
    assert_that(tag_beta).is_equal_to('v1.0.0-beta')

    assert_that(actual_output_prod).is_equal_to(ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='0.0.1',
        previous_version_name='v0.0.1',
        tag_created=True
    ))
    assert_that(tag_prod).is_equal_to('v1.0.0')
