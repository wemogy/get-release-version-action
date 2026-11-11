"""Test that an already existing tag for the computed version is reused instead of failing."""
# pylint: disable=too-many-locals,too-many-statements,duplicate-code,unused-import,redefined-outer-name
from assertpy import assert_that

from test_utils import ActionInputs, ActionOutputs, CommitMessages, logging, TestRepo, repo, run_action


def _prod_inputs() -> ActionInputs:
    """Inputs of a plain release pipeline: no suffixes, semantic bumps and tag creation enabled."""
    return ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        reference_version_suffix=None,
        create_tag=True
    )


def test_existing_tag_on_other_commit_is_reused(repo: TestRepo) -> None:
    """
    Regression: when the tag the action computes already exists, the action must reuse it
    instead of failing with ``fatal: tag 'X' already exists``.

    Scenario:

    1. A ``fix:`` commit is released, producing ``v0.0.1``.
    2. A ``v0.0.2`` tag already exists on an older commit (e.g. created by a previous run of the pipeline whose
       later jobs failed). As the action resolves the current version by commit date, it still sees ``v0.0.1``
       as the current version.
    3. Another ``fix:`` commit is released. The action computes ``v0.0.2`` again, which collides with the
       existing tag. It must report ``v0.0.2`` with ``tag_created`` and leave the existing tag untouched.
    """
    # Arrange
    initial_commit = list(repo.repo.iter_commits('main'))[-1]

    repo.commit(CommitMessages.FIX)
    repo.merge('main', 'release-prod')
    first_output = run_action(_prod_inputs())
    assert_that(first_output.version_name).is_equal_to('v0.0.1')

    # The tag for the next version already exists on an older commit.
    repo.repo.create_tag('v0.0.2', ref=initial_commit.hexsha, message='Release v0.0.2')

    expected_output = ActionOutputs(
        version='0.0.2',
        version_name='v0.0.2',
        previous_version='0.0.1',
        previous_version_name='v0.0.1',
        tag_created=True
    )

    # Act
    repo.checkout('main')
    repo.commit(CommitMessages.FIX)
    repo.merge('main', 'release-prod')
    actual_output = run_action(_prod_inputs())

    # Assert
    assert_that(actual_output).is_equal_to(expected_output)

    # No new tag got created, the already existing one got reused ...
    assert_that(repo.get_latest_tag_name()).is_equal_to('v0.0.1')

    # ... and it still points to the commit it was created on.
    assert_that(repo.repo.tags['v0.0.2'].commit.hexsha).is_equal_to(initial_commit.hexsha)


def test_existing_tag_on_head_is_reused(repo: TestRepo) -> None:
    """
    Regression: a re-run of a pipeline whose tag already points to ``HEAD`` must not fail.

    Scenario:

    1. A ``feat:`` commit is released on ``release-prod``, producing ``v0.1.0`` on its ``HEAD``.
    2. A tag with an older version (``v0.0.1``) exists on a newer commit of another branch. As the action
       resolves the current version by commit date, it sees ``v0.0.1`` as the current version.
    3. The action runs on ``release-prod`` again. It computes ``v0.1.0`` again, which already exists on
       ``HEAD``. It must report ``v0.1.0`` with ``tag_created`` and leave the existing tag untouched.
    """
    # Arrange
    feat_commit = repo.commit(CommitMessages.FEATURE)
    repo.merge('main', 'release-prod')
    first_output = run_action(_prod_inputs())
    assert_that(first_output.version_name).is_equal_to('v0.1.0')

    # An older version is tagged on a newer commit of another branch.
    repo.checkout('release')
    fix_commit = repo.commit(CommitMessages.FIX)
    repo.repo.create_tag('v0.0.1', ref=fix_commit.hexsha, message='Release v0.0.1')

    expected_output = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='0.0.1',
        previous_version_name='v0.0.1',
        tag_created=True
    )

    # Act
    repo.checkout('release-prod')
    actual_output = run_action(_prod_inputs())

    # Assert
    assert_that(actual_output).is_equal_to(expected_output)

    # No new tag got created, the already existing one got reused ...
    assert_that(repo.get_latest_tag_name()).is_equal_to('v0.1.0')

    # ... and it still points to HEAD.
    assert_that(repo.repo.tags['v0.1.0'].commit.hexsha).is_equal_to(feat_commit.hexsha)
