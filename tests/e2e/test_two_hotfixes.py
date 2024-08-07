"""Test all scenarios where two hotfixes / cherrypicks are made."""
# pylint: disable=too-many-locals,too-many-lines,duplicate-code,too-many-statements,unused-import,redefined-outer-name
from assertpy import assert_that

from test_utils import ActionInputs, ActionOutputs, CommitMessages, logging, TestRepo, repo, run_action


def test_fix_then_hotfixes(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` commit and after two hotfixes."""
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

    # Hotfix 1
    args_hotfix1_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix1_release = ActionOutputs(
        version='0.0.1-pre-hotfix.1',
        version_name='v0.0.1-pre-hotfix.1',
        previous_version='0.0.1-pre',
        previous_version_name='v0.0.1-pre',
        tag_created=True
    )

    args_hotfix1_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        reference_version_suffix='pre',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix1_beta = ActionOutputs(
        version='0.0.1-beta-hotfix.1',
        version_name='v0.0.1-beta-hotfix.1',
        previous_version='0.0.1-beta',
        previous_version_name='v0.0.1-beta',
        tag_created=True
    )

    args_hotfix1_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        reference_version_suffix='beta',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix1_prod = ActionOutputs(
        version='0.0.1-hotfix.1',
        version_name='v0.0.1-hotfix.1',
        previous_version='0.0.1',
        previous_version_name='v0.0.1',
        tag_created=True
    )

    # Hotfix 2
    args_hotfix2_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix2_release = ActionOutputs(
        version='0.0.1-pre-hotfix.2',
        version_name='v0.0.1-pre-hotfix.2',
        previous_version='0.0.1-pre-hotfix.1',
        previous_version_name='v0.0.1-pre-hotfix.1',
        tag_created=True
    )

    args_hotfix2_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        reference_version_suffix='pre',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix2_beta = ActionOutputs(
        version='0.0.1-beta-hotfix.2',
        version_name='v0.0.1-beta-hotfix.2',
        previous_version='0.0.1-beta-hotfix.1',
        previous_version_name='v0.0.1-beta-hotfix.1',
        tag_created=True
    )

    args_hotfix2_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        reference_version_suffix='beta',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix2_prod = ActionOutputs(
        version='0.0.1-hotfix.2',
        version_name='v0.0.1-hotfix.2',
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

    # Hotfix 1
    repo.checkout('main')
    commit = repo.commit(CommitMessages.FIX)

    repo.cherrypick(commit, 'release')
    actual_output_hotfix1_release = run_action(args_hotfix1_release)
    tag_hotfix1_release = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-beta')
    actual_output_hotfix1_beta = run_action(args_hotfix1_beta)
    tag_hotfix1_beta = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-prod')
    actual_output_hotfix1_prod = run_action(args_hotfix1_prod)
    tag_hotfix1_prod = repo.get_latest_tag_name()

    # Hotfix 2
    repo.checkout('main')
    commit = repo.commit(CommitMessages.FIX)

    repo.cherrypick(commit, 'release')
    actual_output_hotfix2_release = run_action(args_hotfix2_release)
    tag_hotfix2_release = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-beta')
    actual_output_hotfix2_beta = run_action(args_hotfix2_beta)
    tag_hotfix2_beta = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-prod')
    actual_output_hotfix2_prod = run_action(args_hotfix2_prod)
    tag_hotfix2_prod = repo.get_latest_tag_name()

    # Assert
    # Fix
    assert_that(actual_output_fix_release).is_equal_to(expected_output_fix_release)
    assert_that(tag_fix_release).is_equal_to(expected_output_fix_release.version_name)

    assert_that(actual_output_fix_beta).is_equal_to(expected_output_fix_beta)
    assert_that(tag_fix_beta).is_equal_to(expected_output_fix_beta.version_name)

    assert_that(actual_output_fix_prod).is_equal_to(expected_output_fix_prod)
    assert_that(tag_fix_prod).is_equal_to(expected_output_fix_prod.version_name)

    # Hotfix 1
    assert_that(actual_output_hotfix1_release).is_equal_to(expected_output_hotfix1_release)
    assert_that(tag_hotfix1_release).is_equal_to(expected_output_hotfix1_release.version_name)

    assert_that(actual_output_hotfix1_beta).is_equal_to(expected_output_hotfix1_beta)
    assert_that(tag_hotfix1_beta).is_equal_to(expected_output_hotfix1_beta.version_name)

    assert_that(actual_output_hotfix1_prod).is_equal_to(expected_output_hotfix1_prod)
    assert_that(tag_hotfix1_prod).is_equal_to(expected_output_hotfix1_prod.version_name)

    # Hotfix 2
    assert_that(actual_output_hotfix2_release).is_equal_to(expected_output_hotfix2_release)
    assert_that(tag_hotfix2_release).is_equal_to(expected_output_hotfix2_release.version_name)

    assert_that(actual_output_hotfix2_beta).is_equal_to(expected_output_hotfix2_beta)
    assert_that(tag_hotfix2_beta).is_equal_to(expected_output_hotfix2_beta.version_name)

    assert_that(actual_output_hotfix2_prod).is_equal_to(expected_output_hotfix2_prod)
    assert_that(tag_hotfix2_prod).is_equal_to(expected_output_hotfix2_prod.version_name)


def test_feat_then_hotfixes(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat:`` commit and after two hotfixes."""
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

    # Hotfix 1
    args_hotfix1_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix1_release = ActionOutputs(
        version='0.1.0-pre-hotfix.1',
        version_name='v0.1.0-pre-hotfix.1',
        previous_version='0.1.0-pre',
        previous_version_name='v0.1.0-pre',
        tag_created=True
    )

    args_hotfix1_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        reference_version_suffix='pre',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix1_beta = ActionOutputs(
        version='0.1.0-beta-hotfix.1',
        version_name='v0.1.0-beta-hotfix.1',
        previous_version='0.1.0-beta',
        previous_version_name='v0.1.0-beta',
        tag_created=True
    )

    args_hotfix1_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        reference_version_suffix='beta',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix1_prod = ActionOutputs(
        version='0.1.0-hotfix.1',
        version_name='v0.1.0-hotfix.1',
        previous_version='0.1.0',
        previous_version_name='v0.1.0',
        tag_created=True
    )

    # Hotfix 2
    args_hotfix2_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix2_release = ActionOutputs(
        version='0.1.0-pre-hotfix.2',
        version_name='v0.1.0-pre-hotfix.2',
        previous_version='0.1.0-pre-hotfix.1',
        previous_version_name='v0.1.0-pre-hotfix.1',
        tag_created=True
    )

    args_hotfix2_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        reference_version_suffix='pre',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix2_beta = ActionOutputs(
        version='0.1.0-beta-hotfix.2',
        version_name='v0.1.0-beta-hotfix.2',
        previous_version='0.1.0-beta-hotfix.1',
        previous_version_name='v0.1.0-beta-hotfix.1',
        tag_created=True
    )

    args_hotfix2_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        reference_version_suffix='beta',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix2_prod = ActionOutputs(
        version='0.1.0-hotfix.2',
        version_name='v0.1.0-hotfix.2',
        previous_version='0.1.0-hotfix.1',
        previous_version_name='v0.1.0-hotfix.1',
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

    # Hotfix 1
    repo.checkout('main')
    commit = repo.commit(CommitMessages.FIX)

    repo.cherrypick(commit, 'release')
    actual_output_hotfix1_release = run_action(args_hotfix1_release)
    tag_hotfix1_release = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-beta')
    actual_output_hotfix1_beta = run_action(args_hotfix1_beta)
    tag_hotfix1_beta = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-prod')
    actual_output_hotfix1_prod = run_action(args_hotfix1_prod)
    tag_hotfix1_prod = repo.get_latest_tag_name()

    # Hotfix 2
    repo.checkout('main')
    commit = repo.commit(CommitMessages.FIX)

    repo.cherrypick(commit, 'release')
    actual_output_hotfix2_release = run_action(args_hotfix2_release)
    tag_hotfix2_release = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-beta')
    actual_output_hotfix2_beta = run_action(args_hotfix2_beta)
    tag_hotfix2_beta = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-prod')
    actual_output_hotfix2_prod = run_action(args_hotfix2_prod)
    tag_hotfix2_prod = repo.get_latest_tag_name()

    # Assert
    # Feature
    assert_that(actual_output_feat_release).is_equal_to(expected_output_feat_release)
    assert_that(tag_feat_release).is_equal_to(expected_output_feat_release.version_name)

    assert_that(actual_output_feat_beta).is_equal_to(expected_output_feat_beta)
    assert_that(tag_feat_beta).is_equal_to(expected_output_feat_beta.version_name)

    assert_that(actual_output_feat_prod).is_equal_to(expected_output_feat_prod)
    assert_that(tag_feat_prod).is_equal_to(expected_output_feat_prod.version_name)

    # Hotfix 1
    assert_that(actual_output_hotfix1_release).is_equal_to(expected_output_hotfix1_release)
    assert_that(tag_hotfix1_release).is_equal_to(expected_output_hotfix1_release.version_name)

    assert_that(actual_output_hotfix1_beta).is_equal_to(expected_output_hotfix1_beta)
    assert_that(tag_hotfix1_beta).is_equal_to(expected_output_hotfix1_beta.version_name)

    assert_that(actual_output_hotfix1_prod).is_equal_to(expected_output_hotfix1_prod)
    assert_that(tag_hotfix1_prod).is_equal_to(expected_output_hotfix1_prod.version_name)

    # Hotfix 2
    assert_that(actual_output_hotfix2_release).is_equal_to(expected_output_hotfix2_release)
    assert_that(tag_hotfix2_release).is_equal_to(expected_output_hotfix2_release.version_name)

    assert_that(actual_output_hotfix2_beta).is_equal_to(expected_output_hotfix2_beta)
    assert_that(tag_hotfix2_beta).is_equal_to(expected_output_hotfix2_beta.version_name)

    assert_that(actual_output_hotfix2_prod).is_equal_to(expected_output_hotfix2_prod)
    assert_that(tag_hotfix2_prod).is_equal_to(expected_output_hotfix2_prod.version_name)


def test_breaking_then_hotfixes(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat!:`` commit and after two hotfixes."""
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

    # Hotfix 1
    args_hotfix1_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix1_release = ActionOutputs(
        version='1.0.0-pre-hotfix.1',
        version_name='v1.0.0-pre-hotfix.1',
        previous_version='1.0.0-pre',
        previous_version_name='v1.0.0-pre',
        tag_created=True
    )

    args_hotfix1_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        reference_version_suffix='pre',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix1_beta = ActionOutputs(
        version='1.0.0-beta-hotfix.1',
        version_name='v1.0.0-beta-hotfix.1',
        previous_version='1.0.0-beta',
        previous_version_name='v1.0.0-beta',
        tag_created=True
    )

    args_hotfix1_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        reference_version_suffix='beta',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix1_prod = ActionOutputs(
        version='1.0.0-hotfix.1',
        version_name='v1.0.0-hotfix.1',
        previous_version='1.0.0',
        previous_version_name='v1.0.0',
        tag_created=True
    )

    # Hotfix 2
    args_hotfix2_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix2_release = ActionOutputs(
        version='1.0.0-pre-hotfix.2',
        version_name='v1.0.0-pre-hotfix.2',
        previous_version='1.0.0-pre-hotfix.1',
        previous_version_name='v1.0.0-pre-hotfix.1',
        tag_created=True
    )

    args_hotfix2_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        reference_version_suffix='pre',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix2_beta = ActionOutputs(
        version='1.0.0-beta-hotfix.2',
        version_name='v1.0.0-beta-hotfix.2',
        previous_version='1.0.0-beta-hotfix.1',
        previous_version_name='v1.0.0-beta-hotfix.1',
        tag_created=True
    )

    args_hotfix2_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        reference_version_suffix='beta',
        bumping_suffix='hotfix',
        only_bump_suffix=True,
        create_tag=True
    )

    expected_output_hotfix2_prod = ActionOutputs(
        version='1.0.0-hotfix.2',
        version_name='v1.0.0-hotfix.2',
        previous_version='1.0.0-hotfix.1',
        previous_version_name='v1.0.0-hotfix.1',
        tag_created=True
    )

    # Act
    # Breaking
    repo.commit(CommitMessages.BREAKING_FIX)

    repo.merge('main', 'release')
    actual_output_breaking_release = run_action(args_breaking_release)
    tag_breaking_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_breaking_beta = run_action(args_breaking_beta)
    tag_breaking_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_breaking_prod = run_action(args_breaking_prod)
    tag_breaking_prod = repo.get_latest_tag_name()

    # Hotfix 1
    repo.checkout('main')
    commit = repo.commit(CommitMessages.FIX)

    repo.cherrypick(commit, 'release')
    actual_output_hotfix1_release = run_action(args_hotfix1_release)
    tag_hotfix1_release = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-beta')
    actual_output_hotfix1_beta = run_action(args_hotfix1_beta)
    tag_hotfix1_beta = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-prod')
    actual_output_hotfix1_prod = run_action(args_hotfix1_prod)
    tag_hotfix1_prod = repo.get_latest_tag_name()

    # Hotfix 2
    repo.checkout('main')
    commit = repo.commit(CommitMessages.FIX)

    repo.cherrypick(commit, 'release')
    actual_output_hotfix2_release = run_action(args_hotfix2_release)
    tag_hotfix2_release = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-beta')
    actual_output_hotfix2_beta = run_action(args_hotfix2_beta)
    tag_hotfix2_beta = repo.get_latest_tag_name()

    repo.cherrypick(commit, 'release-prod')
    actual_output_hotfix2_prod = run_action(args_hotfix2_prod)
    tag_hotfix2_prod = repo.get_latest_tag_name()

    # Assert
    # Breaking
    assert_that(actual_output_breaking_release).is_equal_to(expected_output_breaking_release)
    assert_that(tag_breaking_release).is_equal_to(expected_output_breaking_release.version_name)

    assert_that(actual_output_breaking_beta).is_equal_to(expected_output_breaking_beta)
    assert_that(tag_breaking_beta).is_equal_to(expected_output_breaking_beta.version_name)

    assert_that(actual_output_breaking_prod).is_equal_to(expected_output_breaking_prod)
    assert_that(tag_breaking_prod).is_equal_to(expected_output_breaking_prod.version_name)

    # Hotfix 1
    assert_that(actual_output_hotfix1_release).is_equal_to(expected_output_hotfix1_release)
    assert_that(tag_hotfix1_release).is_equal_to(expected_output_hotfix1_release.version_name)

    assert_that(actual_output_hotfix1_beta).is_equal_to(expected_output_hotfix1_beta)
    assert_that(tag_hotfix1_beta).is_equal_to(expected_output_hotfix1_beta.version_name)

    assert_that(actual_output_hotfix1_prod).is_equal_to(expected_output_hotfix1_prod)
    assert_that(tag_hotfix1_prod).is_equal_to(expected_output_hotfix1_prod.version_name)

    # Hotfix 2
    assert_that(actual_output_hotfix2_release).is_equal_to(expected_output_hotfix2_release)
    assert_that(tag_hotfix2_release).is_equal_to(expected_output_hotfix2_release.version_name)

    assert_that(actual_output_hotfix2_beta).is_equal_to(expected_output_hotfix2_beta)
    assert_that(tag_hotfix2_beta).is_equal_to(expected_output_hotfix2_beta.version_name)

    assert_that(actual_output_hotfix2_prod).is_equal_to(expected_output_hotfix2_prod)
    assert_that(tag_hotfix2_prod).is_equal_to(expected_output_hotfix2_prod.version_name)
