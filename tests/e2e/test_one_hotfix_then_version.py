"""Test all scenarios where one hotfix / cherrypick and a commit with a release after each are made."""
# pylint: disable=too-many-locals,too-many-lines,duplicate-code,too-many-statements
from assertpy import assert_that

from test_utils import ActionInputs, ActionOutputs, CommitMessages, logging, TestRepo, repo, run_action


def test_fix_then_hotfix_then_fix(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` commit, after a hotfix and after another ``fix:`` commit."""
    # Arrange
    # Fix 1
    args_fix1_release = ActionInputs(
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

    # Hotfix
    args_hotfix_release = ActionInputs(
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix_release = ActionOutputs(
        version='0.0.1-pre-hotfix.1',
        version_name='v0.0.1-pre-hotfix.1',
        previous_version='0.0.1-pre',
        previous_version_name='v0.0.1-pre',
        tag_created=True
    )

    args_hotfix_beta = ActionInputs(
        prefix='v',
        suffix='beta',
        reference_version_suffix='pre',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix_beta = ActionOutputs(
        version='0.0.1-beta-hotfix.1',
        version_name='v0.0.1-beta-hotfix.1',
        previous_version='0.0.1-beta',
        previous_version_name='v0.0.1-beta',
        tag_created=True
    )

    args_hotfix_prod = ActionInputs(
        prefix='v',
        suffix=None,
        reference_version_suffix='beta',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix_prod = ActionOutputs(
        version='0.0.1-hotfix.1',
        version_name='v0.0.1-hotfix.1',
        previous_version='0.0.1',
        previous_version_name='v0.0.1',
        tag_created=True
    )

    # Fix 2
    args_fix2_release = ActionInputs(
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_fix2_release = ActionOutputs(
        version='0.0.2-pre',
        version_name='v0.0.2-pre',
        previous_version='0.0.1-pre-hotfix.1',
        previous_version_name='v0.0.1-pre-hotfix.1',
        tag_created=True
    )

    args_fix2_beta = ActionInputs(
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_fix2_beta = ActionOutputs(
        version='0.0.2-beta',
        version_name='v0.0.2-beta',
        previous_version='0.0.1-beta-hotfix.1',
        previous_version_name='v0.0.1-beta-hotfix.1',
        tag_created=True
    )

    args_fix2_prod = ActionInputs(
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_fix2_prod = ActionOutputs(
        version='0.0.2',
        version_name='v0.0.2',
        previous_version='0.0.1-hotfix.1',
        previous_version_name='v0.0.1-hotfix.1',
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

    # Hotfix
    repo.checkout('main')
    commit = repo.commit(CommitMessages.FIX)

    repo.cherrypick(commit, 'release')
    actual_output_hotfix_release = run_action(args_hotfix_release)
    tag_hotfix_release = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-beta')
    actual_output_hotfix_beta = run_action(args_hotfix_beta)
    tag_hotfix_beta = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-prod')
    actual_output_hotfix_prod = run_action(args_hotfix_prod)
    tag_hotfix_prod = repo.get_latest_tag_name()

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

    # Hotfix
    assert_that(actual_output_hotfix_release).is_equal_to(expected_output_hotfix_release)
    assert_that(tag_hotfix_release).is_equal_to(expected_output_hotfix_release.version_name)

    assert_that(actual_output_hotfix_beta).is_equal_to(expected_output_hotfix_beta)
    assert_that(tag_hotfix_beta).is_equal_to(expected_output_hotfix_beta.version_name)

    assert_that(actual_output_hotfix_prod).is_equal_to(expected_output_hotfix_prod)
    assert_that(tag_hotfix_prod).is_equal_to(expected_output_hotfix_prod.version_name)

    # Fix 2
    assert_that(actual_output_fix2_release).is_equal_to(expected_output_fix2_release)
    assert_that(tag_fix2_release).is_equal_to(expected_output_fix2_release.version_name)

    assert_that(actual_output_fix2_beta).is_equal_to(expected_output_fix2_beta)
    assert_that(tag_fix2_beta).is_equal_to(expected_output_fix2_beta.version_name)

    assert_that(actual_output_fix2_prod).is_equal_to(expected_output_fix2_prod)
    assert_that(tag_fix2_prod).is_equal_to(expected_output_fix2_prod.version_name)


def test_fix_then_hotfix_then_feature(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` commit, after a hotfix and after a ``feat:`` commit."""
    # Arrange
    # Fix
    args_fix_release = ActionInputs(
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

    # Hotfix
    args_hotfix_release = ActionInputs(
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix_release = ActionOutputs(
        version='0.0.1-pre-hotfix.1',
        version_name='v0.0.1-pre-hotfix.1',
        previous_version='0.0.1-pre',
        previous_version_name='v0.0.1-pre',
        tag_created=True
    )

    args_hotfix_beta = ActionInputs(
        prefix='v',
        suffix='beta',
        reference_version_suffix='pre',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix_beta = ActionOutputs(
        version='0.0.1-beta-hotfix.1',
        version_name='v0.0.1-beta-hotfix.1',
        previous_version='0.0.1-beta',
        previous_version_name='v0.0.1-beta',
        tag_created=True
    )

    args_hotfix_prod = ActionInputs(
        prefix='v',
        suffix=None,
        reference_version_suffix='beta',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix_prod = ActionOutputs(
        version='0.0.1-hotfix.1',
        version_name='v0.0.1-hotfix.1',
        previous_version='0.0.1',
        previous_version_name='v0.0.1',
        tag_created=True
    )

    # Feature
    args_feature_release = ActionInputs(
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_feature_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='0.0.1-pre-hotfix.1',
        previous_version_name='v0.0.1-pre-hotfix.1',
        tag_created=True
    )

    args_feature_beta = ActionInputs(
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_feature_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='0.0.1-beta-hotfix.1',
        previous_version_name='v0.0.1-beta-hotfix.1',
        tag_created=True
    )

    args_feature_prod = ActionInputs(
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_feature_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='0.0.1-hotfix.1',
        previous_version_name='v0.0.1-hotfix.1',
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

    # Hotfix
    repo.checkout('main')
    commit = repo.commit(CommitMessages.FIX)

    repo.cherrypick(commit, 'release')
    actual_output_hotfix_release = run_action(args_hotfix_release)
    tag_hotfix_release = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-beta')
    actual_output_hotfix_beta = run_action(args_hotfix_beta)
    tag_hotfix_beta = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-prod')
    actual_output_hotfix_prod = run_action(args_hotfix_prod)
    tag_hotfix_prod = repo.get_latest_tag_name()

    # Feature
    repo.checkout('main')
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_feature_release = run_action(args_feature_release)
    tag_feature_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_feature_beta = run_action(args_feature_beta)
    tag_feature_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_feature_prod = run_action(args_feature_prod)
    tag_feature_prod = repo.get_latest_tag_name()

    # Assert
    # Fix
    assert_that(actual_output_fix_release).is_equal_to(expected_output_fix_release)
    assert_that(tag_fix_release).is_equal_to(expected_output_fix_release.version_name)

    assert_that(actual_output_fix_beta).is_equal_to(expected_output_fix_beta)
    assert_that(tag_fix_beta).is_equal_to(expected_output_fix_beta.version_name)

    assert_that(actual_output_fix_prod).is_equal_to(expected_output_fix_prod)
    assert_that(tag_fix_prod).is_equal_to(expected_output_fix_prod.version_name)

    # Hotfix
    assert_that(actual_output_hotfix_release).is_equal_to(expected_output_hotfix_release)
    assert_that(tag_hotfix_release).is_equal_to(expected_output_hotfix_release.version_name)

    assert_that(actual_output_hotfix_beta).is_equal_to(expected_output_hotfix_beta)
    assert_that(tag_hotfix_beta).is_equal_to(expected_output_hotfix_beta.version_name)

    assert_that(actual_output_hotfix_prod).is_equal_to(expected_output_hotfix_prod)
    assert_that(tag_hotfix_prod).is_equal_to(expected_output_hotfix_prod.version_name)

    # Feature
    assert_that(actual_output_feature_release).is_equal_to(expected_output_feature_release)
    assert_that(tag_feature_release).is_equal_to(expected_output_feature_release.version_name)

    assert_that(actual_output_feature_beta).is_equal_to(expected_output_feature_beta)
    assert_that(tag_feature_beta).is_equal_to(expected_output_feature_beta.version_name)

    assert_that(actual_output_feature_prod).is_equal_to(expected_output_feature_prod)
    assert_that(tag_feature_prod).is_equal_to(expected_output_feature_prod.version_name)


def test_fix_then_hotfix_then_breaking(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` commit, after a hotfix and after a ``feat!`` commit."""
    # Arrange
    # Fix
    args_fix_release = ActionInputs(
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

    # Hotfix
    args_hotfix_release = ActionInputs(
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix_release = ActionOutputs(
        version='0.0.1-pre-hotfix.1',
        version_name='v0.0.1-pre-hotfix.1',
        previous_version='0.0.1-pre',
        previous_version_name='v0.0.1-pre',
        tag_created=True
    )

    args_hotfix_beta = ActionInputs(
        prefix='v',
        suffix='beta',
        reference_version_suffix='pre',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix_beta = ActionOutputs(
        version='0.0.1-beta-hotfix.1',
        version_name='v0.0.1-beta-hotfix.1',
        previous_version='0.0.1-beta',
        previous_version_name='v0.0.1-beta',
        tag_created=True
    )

    args_hotfix_prod = ActionInputs(
        prefix='v',
        suffix=None,
        reference_version_suffix='beta',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix_prod = ActionOutputs(
        version='0.0.1-hotfix.1',
        version_name='v0.0.1-hotfix.1',
        previous_version='0.0.1',
        previous_version_name='v0.0.1',
        tag_created=True
    )

    # Breaking
    args_breaking_release = ActionInputs(
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_breaking_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='0.0.1-pre-hotfix.1',
        previous_version_name='v0.0.1-pre-hotfix.1',
        tag_created=True
    )

    args_breaking_beta = ActionInputs(
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_breaking_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='0.0.1-beta-hotfix.1',
        previous_version_name='v0.0.1-beta-hotfix.1',
        tag_created=True
    )

    args_breaking_prod = ActionInputs(
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_breaking_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='0.0.1-hotfix.1',
        previous_version_name='v0.0.1-hotfix.1',
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

    # Hotfix
    repo.checkout('main')
    commit = repo.commit(CommitMessages.FIX)

    repo.cherrypick(commit, 'release')
    actual_output_hotfix_release = run_action(args_hotfix_release)
    tag_hotfix_release = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-beta')
    actual_output_hotfix_beta = run_action(args_hotfix_beta)
    tag_hotfix_beta = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-prod')
    actual_output_hotfix_prod = run_action(args_hotfix_prod)
    tag_hotfix_prod = repo.get_latest_tag_name()

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

    # Hotfix
    assert_that(actual_output_hotfix_release).is_equal_to(expected_output_hotfix_release)
    assert_that(tag_hotfix_release).is_equal_to(expected_output_hotfix_release.version_name)

    assert_that(actual_output_hotfix_beta).is_equal_to(expected_output_hotfix_beta)
    assert_that(tag_hotfix_beta).is_equal_to(expected_output_hotfix_beta.version_name)

    assert_that(actual_output_hotfix_prod).is_equal_to(expected_output_hotfix_prod)
    assert_that(tag_hotfix_prod).is_equal_to(expected_output_hotfix_prod.version_name)

    # Breaking
    assert_that(actual_output_breaking_release).is_equal_to(expected_output_breaking_release)
    assert_that(tag_breaking_release).is_equal_to(expected_output_breaking_release.version_name)

    assert_that(actual_output_breaking_beta).is_equal_to(expected_output_breaking_beta)
    assert_that(tag_breaking_beta).is_equal_to(expected_output_breaking_beta.version_name)

    assert_that(actual_output_breaking_prod).is_equal_to(expected_output_breaking_prod)
    assert_that(tag_breaking_prod).is_equal_to(expected_output_breaking_prod.version_name)
