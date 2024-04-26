"""Test all scenarios where two commits with a release after each are made."""
# pylint: disable=too-many-locals,too-many-lines,duplicate-code,too-many-statements,unused-import,redefined-outer-name
from assertpy import assert_that

from test_utils import ActionInputs, ActionOutputs, CommitMessages, logging, TestRepo, repo, run_action


def test_chore_then_chore(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``chore:`` and another ``chore:`` commit."""
    # Arrange
    # Chore 1
    args_chore1_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_chore1_release = ActionOutputs(
        version='0.0.0-pre',
        version_name='v0.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_chore1_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_chore1_beta = ActionOutputs(
        version='0.0.0-beta',
        version_name='v0.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_chore1_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_chore1_prod = ActionOutputs(
        version='0.0.0',
        version_name='v0.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    # Chore 2
    args_chore2_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_chore2_release = ActionOutputs(
        version='0.0.0-pre',
        version_name='v0.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_chore2_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_chore2_beta = ActionOutputs(
        version='0.0.0-beta',
        version_name='v0.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_chore2_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_chore2_prod = ActionOutputs(
        version='0.0.0',
        version_name='v0.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    # Act
    # Chore 1
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_chore1_release = run_action(args_chore1_release)
    tag_chore1_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_chore1_beta = run_action(args_chore1_beta)
    tag_chore1_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_chore1_prod = run_action(args_chore1_prod)
    tag_chore1_prod = repo.get_latest_tag_name()

    # Chore 2
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_chore2_release = run_action(args_chore2_release)
    tag_chore2_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_chore2_beta = run_action(args_chore2_beta)
    tag_chore2_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_chore2_prod = run_action(args_chore2_prod)
    tag_chore2_prod = repo.get_latest_tag_name()

    # Assert
    # Chore 1
    assert_that(actual_output_chore1_release).is_equal_to(expected_output_chore1_release)
    assert_that(tag_chore1_release).is_none()

    assert_that(actual_output_chore1_beta).is_equal_to(expected_output_chore1_beta)
    assert_that(tag_chore1_beta).is_none()

    assert_that(actual_output_chore1_prod).is_equal_to(expected_output_chore1_prod)
    assert_that(tag_chore1_prod).is_none()

    # Chore 2
    assert_that(actual_output_chore2_release).is_equal_to(expected_output_chore2_release)
    assert_that(tag_chore2_release).is_none()

    assert_that(actual_output_chore2_beta).is_equal_to(expected_output_chore2_beta)
    assert_that(tag_chore2_beta).is_none()

    assert_that(actual_output_chore2_prod).is_equal_to(expected_output_chore2_prod)
    assert_that(tag_chore2_prod).is_none()


def test_chore_then_fix(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``chore:`` and a ``fix:`` commit."""
    # Arrange
    # Chore
    args_chore_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_chore_release = ActionOutputs(
        version='0.0.0-pre',
        version_name='v0.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_chore_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_chore_beta = ActionOutputs(
        version='0.0.0-beta',
        version_name='v0.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_chore_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_chore_prod = ActionOutputs(
        version='0.0.0',
        version_name='v0.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    # Fix
    args_fix_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_fix_release = ActionOutputs(
        version='0.0.1-pre',
        version_name='v0.0.1-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_fix_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_fix_beta = ActionOutputs(
        version='0.0.1-beta',
        version_name='v0.0.1-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_fix_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_fix_prod = ActionOutputs(
        version='0.0.1',
        version_name='v0.0.1',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    # Chore
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_chore_release = run_action(args_chore_release)
    tag_chore_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_chore_beta = run_action(args_chore_beta)
    tag_chore_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_chore_prod = run_action(args_chore_prod)
    tag_chore_prod = repo.get_latest_tag_name()

    # Fix
    repo.checkout('main')
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_fix_release = run_action(args_fix_release)
    tag_fix_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_fix_beta = run_action(args_fix_beta)
    tag_fix_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_fix_prod = run_action(args_fix_prod)
    tag_fix_prod = repo.get_latest_tag_name()

    # Assert
    # Chore
    assert_that(actual_output_chore_release).is_equal_to(expected_output_chore_release)
    assert_that(tag_chore_release).is_none()

    assert_that(actual_output_chore_beta).is_equal_to(expected_output_chore_beta)
    assert_that(tag_chore_beta).is_none()

    assert_that(actual_output_chore_prod).is_equal_to(expected_output_chore_prod)
    assert_that(tag_chore_prod).is_none()

    # Fix
    assert_that(actual_output_fix_release).is_equal_to(expected_output_fix_release)
    assert_that(tag_fix_release).is_equal_to(expected_output_fix_release.version_name)

    assert_that(actual_output_fix_beta).is_equal_to(expected_output_fix_beta)
    assert_that(tag_fix_beta).is_equal_to(expected_output_fix_beta.version_name)

    assert_that(actual_output_fix_prod).is_equal_to(expected_output_fix_prod)
    assert_that(tag_fix_prod).is_equal_to(expected_output_fix_prod.version_name)


def test_chore_then_feat(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``chore:`` and a ``feat:`` commit."""
    # Arrange
    # Chore
    args_chore_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_chore_release = ActionOutputs(
        version='0.0.0-pre',
        version_name='v0.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_chore_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_chore_beta = ActionOutputs(
        version='0.0.0-beta',
        version_name='v0.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_chore_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_chore_prod = ActionOutputs(
        version='0.0.0',
        version_name='v0.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    # Feature
    args_feat_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_feat_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_feat_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_feat_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_feat_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_feat_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    # Chore
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_chore_release = run_action(args_chore_release)
    tag_chore_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_chore_beta = run_action(args_chore_beta)
    tag_chore_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_chore_prod = run_action(args_chore_prod)
    tag_chore_prod = repo.get_latest_tag_name()

    # Feature
    repo.checkout('main')
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_feat_release = run_action(args_feat_release)
    tag_feat_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_feat_beta = run_action(args_feat_beta)
    tag_feat_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_feat_prod = run_action(args_feat_prod)
    tag_feat_prod = repo.get_latest_tag_name()

    # Assert
    # Chore
    assert_that(actual_output_chore_release).is_equal_to(expected_output_chore_release)
    assert_that(tag_chore_release).is_none()

    assert_that(actual_output_chore_beta).is_equal_to(expected_output_chore_beta)
    assert_that(tag_chore_beta).is_none()

    assert_that(actual_output_chore_prod).is_equal_to(expected_output_chore_prod)
    assert_that(tag_chore_prod).is_none()

    # Feature
    assert_that(actual_output_feat_release).is_equal_to(expected_output_feat_release)
    assert_that(tag_feat_release).is_equal_to(expected_output_feat_release.version_name)

    assert_that(actual_output_feat_beta).is_equal_to(expected_output_feat_beta)
    assert_that(tag_feat_beta).is_equal_to(expected_output_feat_beta.version_name)

    assert_that(actual_output_feat_prod).is_equal_to(expected_output_feat_prod)
    assert_that(tag_feat_prod).is_equal_to(expected_output_feat_prod.version_name)


def test_chore_then_breaking(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``chore:`` and a ``feat!:`` commit."""
    # Arrange
    # Chore
    args_chore_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_chore_release = ActionOutputs(
        version='0.0.0-pre',
        version_name='v0.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_chore_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_chore_beta = ActionOutputs(
        version='0.0.0-beta',
        version_name='v0.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_chore_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_chore_prod = ActionOutputs(
        version='0.0.0',
        version_name='v0.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    # Breaking
    args_breaking_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_breaking_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_breaking_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_breaking_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_breaking_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_breaking_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    # Chore
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_chore_release = run_action(args_chore_release)
    tag_chore_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_chore_beta = run_action(args_chore_beta)
    tag_chore_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_chore_prod = run_action(args_chore_prod)
    tag_chore_prod = repo.get_latest_tag_name()

    # Breaking
    repo.checkout('main')
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_breaking_release = run_action(args_breaking_release)
    tag_breaking_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_breaking_beta = run_action(args_breaking_beta)
    tag_breaking_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_breaking_prod = run_action(args_breaking_prod)
    tag_breaking_prod = repo.get_latest_tag_name()

    # Assert
    # Chore
    assert_that(actual_output_chore_release).is_equal_to(expected_output_chore_release)
    assert_that(tag_chore_release).is_none()

    assert_that(actual_output_chore_beta).is_equal_to(expected_output_chore_beta)
    assert_that(tag_chore_beta).is_none()

    assert_that(actual_output_chore_prod).is_equal_to(expected_output_chore_prod)
    assert_that(tag_chore_prod).is_none()

    # Breaking
    assert_that(actual_output_breaking_release).is_equal_to(expected_output_breaking_release)
    assert_that(tag_breaking_release).is_equal_to(expected_output_breaking_release.version_name)

    assert_that(actual_output_breaking_beta).is_equal_to(expected_output_breaking_beta)
    assert_that(tag_breaking_beta).is_equal_to(expected_output_breaking_beta.version_name)

    assert_that(actual_output_breaking_prod).is_equal_to(expected_output_breaking_prod)
    assert_that(tag_breaking_prod).is_equal_to(expected_output_breaking_prod.version_name)


def test_fix_then_chore(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` and a ``chore:`` commit."""
    # Arrange
    # Fix
    args_fix_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_fix_release = ActionOutputs(
        version='0.0.1-pre',
        version_name='v0.0.1-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_fix_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_fix_beta = ActionOutputs(
        version='0.0.1-beta',
        version_name='v0.0.1-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_fix_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_fix_prod = ActionOutputs(
        version='0.0.1',
        version_name='v0.0.1',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Chore
    args_chore_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_chore_release = ActionOutputs(
        version='0.0.1-pre',
        version_name='v0.0.1-pre',
        previous_version='0.0.1-pre',
        previous_version_name='v0.0.1-pre',
        tag_created=False
    )

    args_chore_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_chore_beta = ActionOutputs(
        version='0.0.1-beta',
        version_name='v0.0.1-beta',
        previous_version='0.0.1-beta',
        previous_version_name='v0.0.1-beta',
        tag_created=False
    )

    args_chore_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_chore_prod = ActionOutputs(
        version='0.0.1',
        version_name='v0.0.1',
        previous_version='0.0.1',
        previous_version_name='v0.0.1',
        tag_created=False
    )

    # Act
    # Fix
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_fix_release = run_action(args_fix_release)
    tag_fix_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_fix_beta = run_action(args_fix_beta)
    tag_fix_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_fix_prod = run_action(args_fix_prod)
    tag_fix_prod = repo.get_latest_tag_name()

    # Chore
    repo.checkout('main')
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_chore_release = run_action(args_chore_release)
    tag_chore_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_chore_beta = run_action(args_chore_beta)
    tag_chore_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_chore_prod = run_action(args_chore_prod)
    tag_chore_prod = repo.get_latest_tag_name()

    # Assert
    # Fix
    assert_that(actual_output_fix_release).is_equal_to(expected_output_fix_release)
    assert_that(tag_fix_release).is_equal_to(expected_output_fix_release.version_name)

    assert_that(actual_output_fix_beta).is_equal_to(expected_output_fix_beta)
    assert_that(tag_fix_beta).is_equal_to(expected_output_fix_beta.version_name)

    assert_that(actual_output_fix_prod).is_equal_to(expected_output_fix_prod)
    assert_that(tag_fix_prod).is_equal_to(expected_output_fix_prod.version_name)

    # Chore
    assert_that(actual_output_chore_release).is_equal_to(expected_output_chore_release)
    assert_that(tag_chore_release).is_equal_to(expected_output_fix_prod.version_name)

    assert_that(actual_output_chore_beta).is_equal_to(expected_output_chore_beta)
    assert_that(tag_chore_beta).is_equal_to(expected_output_fix_prod.version_name)

    assert_that(actual_output_chore_prod).is_equal_to(expected_output_chore_prod)
    assert_that(tag_chore_prod).is_equal_to(expected_output_fix_prod.version_name)


def test_fix_then_fix(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` and another ``fix:`` commit."""
    # Arrange
    # Fix 1
    args_fix1_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_fix1_release = ActionOutputs(
        version='0.0.1-pre',
        version_name='v0.0.1-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_fix1_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_fix1_beta = ActionOutputs(
        version='0.0.1-beta',
        version_name='v0.0.1-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_fix1_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_fix1_prod = ActionOutputs(
        version='0.0.1',
        version_name='v0.0.1',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Fix 2
    args_fix2_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_fix2_release = ActionOutputs(
        version='0.0.2-pre',
        version_name='v0.0.2-pre',
        previous_version='0.0.1-pre',
        previous_version_name='v0.0.1-pre',
        tag_created=True
    )

    args_fix2_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_fix2_beta = ActionOutputs(
        version='0.0.2-beta',
        version_name='v0.0.2-beta',
        previous_version='0.0.1-beta',
        previous_version_name='v0.0.1-beta',
        tag_created=True
    )

    args_fix2_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_fix2_prod = ActionOutputs(
        version='0.0.2',
        version_name='v0.0.2',
        previous_version='0.0.1',
        previous_version_name='v0.0.1',
        tag_created=True
    )

    # Act
    # Fix 1
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_fix1_release = run_action(args_fix1_release)
    tag_fix1_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_fix1_beta = run_action(args_fix1_beta)
    tag_fix1_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_fix1_prod = run_action(args_fix1_prod)
    tag_fix1_prod = repo.get_latest_tag_name()

    # Fix 2
    repo.checkout('main')
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_fix2_release = run_action(args_fix2_release)
    tag_fix2_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_fix2_beta = run_action(args_fix2_beta)
    tag_fix2_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_fix2_prod = run_action(args_fix2_prod)
    tag_fix2_prod = repo.get_latest_tag_name()

    # Assert
    # Fix 1
    assert_that(actual_output_fix1_release).is_equal_to(expected_output_fix1_release)
    assert_that(tag_fix1_release).is_equal_to(expected_output_fix1_release.version_name)

    assert_that(actual_output_fix1_beta).is_equal_to(expected_output_fix1_beta)
    assert_that(tag_fix1_beta).is_equal_to(expected_output_fix1_beta.version_name)

    assert_that(actual_output_fix1_prod).is_equal_to(expected_output_fix1_prod)
    assert_that(tag_fix1_prod).is_equal_to(expected_output_fix1_prod.version_name)

    # Fix 2
    assert_that(actual_output_fix2_release).is_equal_to(expected_output_fix2_release)
    assert_that(tag_fix2_release).is_equal_to(expected_output_fix2_release.version_name)

    assert_that(actual_output_fix2_beta).is_equal_to(expected_output_fix2_beta)
    assert_that(tag_fix2_beta).is_equal_to(expected_output_fix2_beta.version_name)

    assert_that(actual_output_fix2_prod).is_equal_to(expected_output_fix2_prod)
    assert_that(tag_fix2_prod).is_equal_to(expected_output_fix2_prod.version_name)


def test_fix_then_feat(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` and a ``feat:`` commit."""
    # Arrange
    # Fix
    args_fix_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_fix_release = ActionOutputs(
        version='0.0.1-pre',
        version_name='v0.0.1-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_fix_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_fix_beta = ActionOutputs(
        version='0.0.1-beta',
        version_name='v0.0.1-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_fix_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_fix_prod = ActionOutputs(
        version='0.0.1',
        version_name='v0.0.1',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Feature
    args_feat_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_feat_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='0.0.1-pre',
        previous_version_name='v0.0.1-pre',
        tag_created=True
    )

    args_feat_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_feat_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='0.0.1-beta',
        previous_version_name='v0.0.1-beta',
        tag_created=True
    )

    args_feat_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_feat_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='0.0.1',
        previous_version_name='v0.0.1',
        tag_created=True
    )

    # Act
    # Fix
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_fix_release = run_action(args_fix_release)
    tag_fix_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_fix_beta = run_action(args_fix_beta)
    tag_fix_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_fix_prod = run_action(args_fix_prod)
    tag_fix_prod = repo.get_latest_tag_name()

    # Feature
    repo.checkout('main')
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_feat_release = run_action(args_feat_release)
    tag_feat_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_feat_beta = run_action(args_feat_beta)
    tag_feat_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_feat_prod = run_action(args_feat_prod)
    tag_feat_prod = repo.get_latest_tag_name()

    # Assert
    # Fix
    assert_that(actual_output_fix_release).is_equal_to(expected_output_fix_release)
    assert_that(tag_fix_release).is_equal_to(expected_output_fix_release.version_name)

    assert_that(actual_output_fix_beta).is_equal_to(expected_output_fix_beta)
    assert_that(tag_fix_beta).is_equal_to(expected_output_fix_beta.version_name)

    assert_that(actual_output_fix_prod).is_equal_to(expected_output_fix_prod)
    assert_that(tag_fix_prod).is_equal_to(expected_output_fix_prod.version_name)

    # Feature
    assert_that(actual_output_feat_release).is_equal_to(expected_output_feat_release)
    assert_that(tag_feat_release).is_equal_to(expected_output_feat_release.version_name)

    assert_that(actual_output_feat_beta).is_equal_to(expected_output_feat_beta)
    assert_that(tag_feat_beta).is_equal_to(expected_output_feat_beta.version_name)

    assert_that(actual_output_feat_prod).is_equal_to(expected_output_feat_prod)
    assert_that(tag_feat_prod).is_equal_to(expected_output_feat_prod.version_name)


def test_fix_then_breaking(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` and a ``feat!:`` commit."""
    # Arrange
    # Fix
    args_fix_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_fix_release = ActionOutputs(
        version='0.0.1-pre',
        version_name='v0.0.1-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_fix_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_fix_beta = ActionOutputs(
        version='0.0.1-beta',
        version_name='v0.0.1-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_fix_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_fix_prod = ActionOutputs(
        version='0.0.1',
        version_name='v0.0.1',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Breaking
    args_breaking_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_breaking_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='0.0.1-pre',
        previous_version_name='v0.0.1-pre',
        tag_created=True
    )

    args_breaking_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_breaking_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='0.0.1-beta',
        previous_version_name='v0.0.1-beta',
        tag_created=True
    )

    args_breaking_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_breaking_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='0.0.1',
        previous_version_name='v0.0.1',
        tag_created=True
    )

    # Act
    # Fix
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_fix_release = run_action(args_fix_release)
    tag_fix_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_fix_beta = run_action(args_fix_beta)
    tag_fix_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_fix_prod = run_action(args_fix_prod)
    tag_fix_prod = repo.get_latest_tag_name()

    # Breaking
    repo.checkout('main')
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_breaking_release = run_action(args_breaking_release)
    tag_breaking_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_breaking_beta = run_action(args_breaking_beta)
    tag_breaking_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_breaking_prod = run_action(args_breaking_prod)
    tag_breaking_prod = repo.get_latest_tag_name()

    # Assert
    # Fix
    assert_that(actual_output_fix_release).is_equal_to(expected_output_fix_release)
    assert_that(tag_fix_release).is_equal_to(expected_output_fix_release.version_name)

    assert_that(actual_output_fix_beta).is_equal_to(expected_output_fix_beta)
    assert_that(tag_fix_beta).is_equal_to(expected_output_fix_beta.version_name)

    assert_that(actual_output_fix_prod).is_equal_to(expected_output_fix_prod)
    assert_that(tag_fix_prod).is_equal_to(expected_output_fix_prod.version_name)

    # Breaking
    assert_that(actual_output_breaking_release).is_equal_to(expected_output_breaking_release)
    assert_that(tag_breaking_release).is_equal_to(expected_output_breaking_release.version_name)

    assert_that(actual_output_breaking_beta).is_equal_to(expected_output_breaking_beta)
    assert_that(tag_breaking_beta).is_equal_to(expected_output_breaking_beta.version_name)

    assert_that(actual_output_breaking_prod).is_equal_to(expected_output_breaking_prod)
    assert_that(tag_breaking_prod).is_equal_to(expected_output_breaking_prod.version_name)


def test_feat_then_chore(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat:`` and a ``chore:`` commit."""
    # Arrange
    # Feature
    args_feat_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_feat_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_feat_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_feat_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_feat_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_feat_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Chore
    args_chore_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_chore_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='0.1.0-pre',
        previous_version_name='v0.1.0-pre',
        tag_created=False
    )

    args_chore_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_chore_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='0.1.0-beta',
        previous_version_name='v0.1.0-beta',
        tag_created=False
    )

    args_chore_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_chore_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='0.1.0',
        previous_version_name='v0.1.0',
        tag_created=False
    )

    # Act
    # Feature
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_feat_release = run_action(args_feat_release)
    tag_feat_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_feat_beta = run_action(args_feat_beta)
    tag_feat_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_feat_prod = run_action(args_feat_prod)
    tag_feat_prod = repo.get_latest_tag_name()

    # Chore
    repo.checkout('main')
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_chore_release = run_action(args_chore_release)
    tag_chore_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_chore_beta = run_action(args_chore_beta)
    tag_chore_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_chore_prod = run_action(args_chore_prod)
    tag_chore_prod = repo.get_latest_tag_name()

    # Assert
    # Feature
    assert_that(actual_output_feat_release).is_equal_to(expected_output_feat_release)
    assert_that(tag_feat_release).is_equal_to(expected_output_feat_release.version_name)

    assert_that(actual_output_feat_beta).is_equal_to(expected_output_feat_beta)
    assert_that(tag_feat_beta).is_equal_to(expected_output_feat_beta.version_name)

    assert_that(actual_output_feat_prod).is_equal_to(expected_output_feat_prod)
    assert_that(tag_feat_prod).is_equal_to(expected_output_feat_prod.version_name)

    # Chore
    assert_that(actual_output_chore_release).is_equal_to(expected_output_chore_release)
    assert_that(tag_chore_release).is_equal_to(expected_output_feat_prod.version_name)

    assert_that(actual_output_chore_beta).is_equal_to(expected_output_chore_beta)
    assert_that(tag_chore_beta).is_equal_to(expected_output_feat_prod.version_name)

    assert_that(actual_output_chore_prod).is_equal_to(expected_output_chore_prod)
    assert_that(tag_chore_prod).is_equal_to(expected_output_feat_prod.version_name)


def test_feat_then_fix(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat:`` and a ``fix:`` commit."""
    # Arrange
    # Feature
    args_feat_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_feat_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_feat_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_feat_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_feat_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_feat_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Fix
    args_fix_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_fix_release = ActionOutputs(
        version='0.1.1-pre',
        version_name='v0.1.1-pre',
        previous_version='0.1.0-pre',
        previous_version_name='v0.1.0-pre',
        tag_created=True
    )

    args_fix_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_fix_beta = ActionOutputs(
        version='0.1.1-beta',
        version_name='v0.1.1-beta',
        previous_version='0.1.0-beta',
        previous_version_name='v0.1.0-beta',
        tag_created=True
    )

    args_fix_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_fix_prod = ActionOutputs(
        version='0.1.1',
        version_name='v0.1.1',
        previous_version='0.1.0',
        previous_version_name='v0.1.0',
        tag_created=True
    )

    # Act
    # Feature
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_feat_release = run_action(args_feat_release)
    tag_feat_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_feat_beta = run_action(args_feat_beta)
    tag_feat_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_feat_prod = run_action(args_feat_prod)
    tag_feat_prod = repo.get_latest_tag_name()

    # Fix
    repo.checkout('main')
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_fix_release = run_action(args_fix_release)
    tag_fix_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_fix_beta = run_action(args_fix_beta)
    tag_fix_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_fix_prod = run_action(args_fix_prod)
    tag_fix_prod = repo.get_latest_tag_name()

    # Assert
    # Feature
    assert_that(actual_output_feat_release).is_equal_to(expected_output_feat_release)
    assert_that(tag_feat_release).is_equal_to(expected_output_feat_release.version_name)

    assert_that(actual_output_feat_beta).is_equal_to(expected_output_feat_beta)
    assert_that(tag_feat_beta).is_equal_to(expected_output_feat_beta.version_name)

    assert_that(actual_output_feat_prod).is_equal_to(expected_output_feat_prod)
    assert_that(tag_feat_prod).is_equal_to(expected_output_feat_prod.version_name)

    # Fix
    assert_that(actual_output_fix_release).is_equal_to(expected_output_fix_release)
    assert_that(tag_fix_release).is_equal_to(expected_output_fix_release.version_name)

    assert_that(actual_output_fix_beta).is_equal_to(expected_output_fix_beta)
    assert_that(tag_fix_beta).is_equal_to(expected_output_fix_beta.version_name)

    assert_that(actual_output_fix_prod).is_equal_to(expected_output_fix_prod)
    assert_that(tag_fix_prod).is_equal_to(expected_output_fix_prod.version_name)


def test_feat_then_feat(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat:`` and another ``feat:`` commit."""
    # Arrange
    # Feature 1
    args_feat1_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_feat1_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_feat1_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_feat1_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_feat1_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_feat1_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Feature 2
    args_feat2_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_feat2_release = ActionOutputs(
        version='0.2.0-pre',
        version_name='v0.2.0-pre',
        previous_version='0.1.0-pre',
        previous_version_name='v0.1.0-pre',
        tag_created=True
    )

    args_feat2_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_feat2_beta = ActionOutputs(
        version='0.2.0-beta',
        version_name='v0.2.0-beta',
        previous_version='0.1.0-beta',
        previous_version_name='v0.1.0-beta',
        tag_created=True
    )

    args_feat2_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True,
    )

    expected_output_feat2_prod = ActionOutputs(
        version='0.2.0',
        version_name='v0.2.0',
        previous_version='0.1.0',
        previous_version_name='v0.1.0',
        tag_created=True
    )

    # Act
    # Feature 1
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_feat1_release = run_action(args_feat1_release)
    tag_feat1_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_feat1_beta = run_action(args_feat1_beta)
    tag_feat1_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_feat1_prod = run_action(args_feat1_prod)
    tag_feat1_prod = repo.get_latest_tag_name()

    # Feature 2
    repo.checkout('main')
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_feat2_release = run_action(args_feat2_release)
    tag_feat2_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_feat2_beta = run_action(args_feat2_beta)
    tag_feat2_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_feat2_prod = run_action(args_feat2_prod)
    tag_feat2_prod = repo.get_latest_tag_name()

    # Assert
    # Feature 1
    assert_that(actual_output_feat1_release).is_equal_to(expected_output_feat1_release)
    assert_that(tag_feat1_release).is_equal_to(expected_output_feat1_release.version_name)

    assert_that(actual_output_feat1_beta).is_equal_to(expected_output_feat1_beta)
    assert_that(tag_feat1_beta).is_equal_to(expected_output_feat1_beta.version_name)

    assert_that(actual_output_feat1_prod).is_equal_to(expected_output_feat1_prod)
    assert_that(tag_feat1_prod).is_equal_to(expected_output_feat1_prod.version_name)

    # Feature 2
    assert_that(actual_output_feat2_release).is_equal_to(expected_output_feat2_release)
    assert_that(tag_feat2_release).is_equal_to(expected_output_feat2_release.version_name)

    assert_that(actual_output_feat2_beta).is_equal_to(expected_output_feat2_beta)
    assert_that(tag_feat2_beta).is_equal_to(expected_output_feat2_beta.version_name)

    assert_that(actual_output_feat2_prod).is_equal_to(expected_output_feat2_prod)
    assert_that(tag_feat2_prod).is_equal_to(expected_output_feat2_prod.version_name)


def test_feat_then_breaking(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat:`` and a ``feat!:`` commit."""
    # Arrange
    # Feature
    args_feat_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_feat_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_feat_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_feat_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_feat_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_feat_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Breaking
    args_breaking_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_breaking_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='0.1.0-pre',
        previous_version_name='v0.1.0-pre',
        tag_created=True
    )

    args_breaking_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_breaking_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='0.1.0-beta',
        previous_version_name='v0.1.0-beta',
        tag_created=True
    )

    args_breaking_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_breaking_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='0.1.0',
        previous_version_name='v0.1.0',
        tag_created=True
    )

    # Act
    # Feature
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_feat_release = run_action(args_feat_release)
    tag_feat_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_feat_beta = run_action(args_feat_beta)
    tag_feat_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_feat_prod = run_action(args_feat_prod)
    tag_feat_prod = repo.get_latest_tag_name()

    # Breaking
    repo.checkout('main')
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_breaking_release = run_action(args_breaking_release)
    tag_breaking_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_breaking_beta = run_action(args_breaking_beta)
    tag_breaking_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_breaking_prod = run_action(args_breaking_prod)
    tag_breaking_prod = repo.get_latest_tag_name()

    # Assert
    # Feature
    assert_that(actual_output_feat_release).is_equal_to(expected_output_feat_release)
    assert_that(tag_feat_release).is_equal_to(expected_output_feat_release.version_name)

    assert_that(actual_output_feat_beta).is_equal_to(expected_output_feat_beta)
    assert_that(tag_feat_beta).is_equal_to(expected_output_feat_beta.version_name)

    assert_that(actual_output_feat_prod).is_equal_to(expected_output_feat_prod)
    assert_that(tag_feat_prod).is_equal_to(expected_output_feat_prod.version_name)

    # Breaking
    assert_that(actual_output_breaking_release).is_equal_to(expected_output_breaking_release)
    assert_that(tag_breaking_release).is_equal_to(expected_output_breaking_release.version_name)

    assert_that(actual_output_breaking_beta).is_equal_to(expected_output_breaking_beta)
    assert_that(tag_breaking_beta).is_equal_to(expected_output_breaking_beta.version_name)

    assert_that(actual_output_breaking_prod).is_equal_to(expected_output_breaking_prod)
    assert_that(tag_breaking_prod).is_equal_to(expected_output_breaking_prod.version_name)


def test_breaking_then_chore(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat!:`` and a ``chore:`` commit."""
    # Arrange
    # Breaking
    args_breaking_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_breaking_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_breaking_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_breaking_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_breaking_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_breaking_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Chore
    args_chore_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_chore_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='1.0.0-pre',
        previous_version_name='v1.0.0-pre',
        tag_created=False
    )

    args_chore_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_chore_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='1.0.0-beta',
        previous_version_name='v1.0.0-beta',
        tag_created=False
    )

    args_chore_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_chore_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='1.0.0',
        previous_version_name='v1.0.0',
        tag_created=False
    )

    # Act
    # Breaking
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_breaking_release = run_action(args_breaking_release)
    tag_breaking_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_breaking_beta = run_action(args_breaking_beta)
    tag_breaking_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_breaking_prod = run_action(args_breaking_prod)
    tag_breaking_prod = repo.get_latest_tag_name()

    # Chore
    repo.checkout('main')
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_chore_release = run_action(args_chore_release)
    tag_chore_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_chore_beta = run_action(args_chore_beta)
    tag_chore_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_chore_prod = run_action(args_chore_prod)
    tag_chore_prod = repo.get_latest_tag_name()

    # Assert
    # Breaking
    assert_that(actual_output_breaking_release).is_equal_to(expected_output_breaking_release)
    assert_that(tag_breaking_release).is_equal_to(expected_output_breaking_release.version_name)

    assert_that(actual_output_breaking_beta).is_equal_to(expected_output_breaking_beta)
    assert_that(tag_breaking_beta).is_equal_to(expected_output_breaking_beta.version_name)

    assert_that(actual_output_breaking_prod).is_equal_to(expected_output_breaking_prod)
    assert_that(tag_breaking_prod).is_equal_to(expected_output_breaking_prod.version_name)

    # Chore
    assert_that(actual_output_chore_release).is_equal_to(expected_output_chore_release)
    assert_that(tag_chore_release).is_equal_to(expected_output_breaking_prod.version_name)

    assert_that(actual_output_chore_beta).is_equal_to(expected_output_chore_beta)
    assert_that(tag_chore_beta).is_equal_to(expected_output_breaking_prod.version_name)

    assert_that(actual_output_chore_prod).is_equal_to(expected_output_chore_prod)
    assert_that(tag_chore_prod).is_equal_to(expected_output_breaking_prod.version_name)


def test_breaking_then_fix(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat!:`` and a ``fix:`` commit."""
    # Arrange
    # Breaking
    args_breaking_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_breaking_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_breaking_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_breaking_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_breaking_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_breaking_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Fix
    args_fix_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_fix_release = ActionOutputs(
        version='1.0.1-pre',
        version_name='v1.0.1-pre',
        previous_version='1.0.0-pre',
        previous_version_name='v1.0.0-pre',
        tag_created=True
    )

    args_fix_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_fix_beta = ActionOutputs(
        version='1.0.1-beta',
        version_name='v1.0.1-beta',
        previous_version='1.0.0-beta',
        previous_version_name='v1.0.0-beta',
        tag_created=True
    )

    args_fix_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_fix_prod = ActionOutputs(
        version='1.0.1',
        version_name='v1.0.1',
        previous_version='1.0.0',
        previous_version_name='v1.0.0',
        tag_created=True
    )

    # Act
    # Breaking
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_breaking_release = run_action(args_breaking_release)
    tag_breaking_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_breaking_beta = run_action(args_breaking_beta)
    tag_breaking_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_breaking_prod = run_action(args_breaking_prod)
    tag_breaking_prod = repo.get_latest_tag_name()

    # Fix
    repo.checkout('main')
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_fix_release = run_action(args_fix_release)
    tag_fix_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_fix_beta = run_action(args_fix_beta)
    tag_fix_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_fix_prod = run_action(args_fix_prod)
    tag_fix_prod = repo.get_latest_tag_name()

    # Assert
    # Breaking
    assert_that(actual_output_breaking_release).is_equal_to(expected_output_breaking_release)
    assert_that(tag_breaking_release).is_equal_to(expected_output_breaking_release.version_name)

    assert_that(actual_output_breaking_beta).is_equal_to(expected_output_breaking_beta)
    assert_that(tag_breaking_beta).is_equal_to(expected_output_breaking_beta.version_name)

    assert_that(actual_output_breaking_prod).is_equal_to(expected_output_breaking_prod)
    assert_that(tag_breaking_prod).is_equal_to(expected_output_breaking_prod.version_name)

    # Fix
    assert_that(actual_output_fix_release).is_equal_to(expected_output_fix_release)
    assert_that(tag_fix_release).is_equal_to(expected_output_fix_release.version_name)

    assert_that(actual_output_fix_beta).is_equal_to(expected_output_fix_beta)
    assert_that(tag_fix_beta).is_equal_to(expected_output_fix_beta.version_name)

    assert_that(actual_output_fix_prod).is_equal_to(expected_output_fix_prod)
    assert_that(tag_fix_prod).is_equal_to(expected_output_fix_prod.version_name)


def test_breaking_then_feat(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat!:`` and a ``feat:`` commit."""
    # Arrange
    # Breaking
    args_breaking_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_breaking_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_breaking_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_breaking_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_breaking_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_breaking_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Feature
    args_feat_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_feat_release = ActionOutputs(
        version='1.1.0-pre',
        version_name='v1.1.0-pre',
        previous_version='1.0.0-pre',
        previous_version_name='v1.0.0-pre',
        tag_created=True
    )

    args_feat_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_feat_beta = ActionOutputs(
        version='1.1.0-beta',
        version_name='v1.1.0-beta',
        previous_version='1.0.0-beta',
        previous_version_name='v1.0.0-beta',
        tag_created=True
    )

    args_feat_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_feat_prod = ActionOutputs(
        version='1.1.0',
        version_name='v1.1.0',
        previous_version='1.0.0',
        previous_version_name='v1.0.0',
        tag_created=True
    )

    # Act
    # Breaking
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_breaking_release = run_action(args_breaking_release)
    tag_breaking_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_breaking_beta = run_action(args_breaking_beta)
    tag_breaking_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_breaking_prod = run_action(args_breaking_prod)
    tag_breaking_prod = repo.get_latest_tag_name()

    # Feature
    repo.checkout('main')
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_feat_release = run_action(args_feat_release)
    tag_feat_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_feat_beta = run_action(args_feat_beta)
    tag_feat_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_feat_prod = run_action(args_feat_prod)
    tag_feat_prod = repo.get_latest_tag_name()

    # Assert
    # Breaking
    assert_that(actual_output_breaking_release).is_equal_to(expected_output_breaking_release)
    assert_that(tag_breaking_release).is_equal_to(expected_output_breaking_release.version_name)

    assert_that(actual_output_breaking_beta).is_equal_to(expected_output_breaking_beta)
    assert_that(tag_breaking_beta).is_equal_to(expected_output_breaking_beta.version_name)

    assert_that(actual_output_breaking_prod).is_equal_to(expected_output_breaking_prod)
    assert_that(tag_breaking_prod).is_equal_to(expected_output_breaking_prod.version_name)

    # Feature
    assert_that(actual_output_feat_release).is_equal_to(expected_output_feat_release)
    assert_that(tag_feat_release).is_equal_to(expected_output_feat_release.version_name)

    assert_that(actual_output_feat_beta).is_equal_to(expected_output_feat_beta)
    assert_that(tag_feat_beta).is_equal_to(expected_output_feat_beta.version_name)

    assert_that(actual_output_feat_prod).is_equal_to(expected_output_feat_prod)
    assert_that(tag_feat_prod).is_equal_to(expected_output_feat_prod.version_name)


def test_breaking_then_breaking(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat!:`` and another ``feat!:`` commit."""
    # Arrange
    # Breaking 1
    args_breaking1_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_breaking1_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_breaking1_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_breaking1_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_breaking1_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_breaking1_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Breaking 2
    args_breaking2_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_breaking2_release = ActionOutputs(
        version='2.0.0-pre',
        version_name='v2.0.0-pre',
        previous_version='1.0.0-pre',
        previous_version_name='v1.0.0-pre',
        tag_created=True
    )

    args_breaking2_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_breaking2_beta = ActionOutputs(
        version='2.0.0-beta',
        version_name='v2.0.0-beta',
        previous_version='1.0.0-beta',
        previous_version_name='v1.0.0-beta',
        tag_created=True
    )

    args_breaking2_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_breaking2_prod = ActionOutputs(
        version='2.0.0',
        version_name='v2.0.0',
        previous_version='1.0.0',
        previous_version_name='v1.0.0',
        tag_created=True
    )

    # Act
    # Breaking 1
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_breaking1_release = run_action(args_breaking1_release)
    tag_breaking1_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_breaking1_beta = run_action(args_breaking1_beta)
    tag_breaking1_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_breaking1_prod = run_action(args_breaking1_prod)
    tag_breaking1_prod = repo.get_latest_tag_name()

    # Breaking 2
    repo.checkout('main')
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_breaking2_release = run_action(args_breaking2_release)
    tag_breaking2_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_breaking2_beta = run_action(args_breaking2_beta)
    tag_breaking2_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_breaking2_prod = run_action(args_breaking2_prod)
    tag_breaking2_prod = repo.get_latest_tag_name()

    # Assert
    # Breaking 1
    assert_that(actual_output_breaking1_release).is_equal_to(expected_output_breaking1_release)
    assert_that(tag_breaking1_release).is_equal_to(expected_output_breaking1_release.version_name)

    assert_that(actual_output_breaking1_beta).is_equal_to(expected_output_breaking1_beta)
    assert_that(tag_breaking1_beta).is_equal_to(expected_output_breaking1_beta.version_name)

    assert_that(actual_output_breaking1_prod).is_equal_to(expected_output_breaking1_prod)
    assert_that(tag_breaking1_prod).is_equal_to(expected_output_breaking1_prod.version_name)

    # Breaking 2
    assert_that(actual_output_breaking2_release).is_equal_to(expected_output_breaking2_release)
    assert_that(tag_breaking2_release).is_equal_to(expected_output_breaking2_release.version_name)

    assert_that(actual_output_breaking2_beta).is_equal_to(expected_output_breaking2_beta)
    assert_that(tag_breaking2_beta).is_equal_to(expected_output_breaking2_beta.version_name)

    assert_that(actual_output_breaking2_prod).is_equal_to(expected_output_breaking2_prod)
    assert_that(tag_breaking2_prod).is_equal_to(expected_output_breaking2_prod.version_name)
