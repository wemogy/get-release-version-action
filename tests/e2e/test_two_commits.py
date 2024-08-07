"""Test all scenarios where two commits with a release at the end are made."""
# pylint: disable=too-many-locals,too-many-lines,duplicate-code,too-many-statements,unused-import,redefined-outer-name

from assertpy import assert_that

from test_utils import ActionInputs, ActionOutputs, CommitMessages, logging, TestRepo, repo, run_action


def test_chore_then_chore(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``chore:`` and another ``chore:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='0.0.0-pre',
        version_name='v0.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='0.0.0-beta',
        version_name='v0.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='0.0.0',
        version_name='v0.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=False
    )

    # Act
    repo.commit(CommitMessages.CHORE)
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_none()

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_none()

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_none()


def test_chore_then_fix(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``chore:`` and a ``fix:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='0.0.1-pre',
        version_name='v0.0.1-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='0.0.1-beta',
        version_name='v0.0.1-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='0.0.1',
        version_name='v0.0.1',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.CHORE)
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_chore_then_feat(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``chore:`` and a ``feat:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.CHORE)
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_chore_then_breaking(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``chore:`` and a ``feat!:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.CHORE)
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_fix_then_chore(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` and a ``chore:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='0.0.1-pre',
        version_name='v0.0.1-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='0.0.1-beta',
        version_name='v0.0.1-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='0.0.1',
        version_name='v0.0.1',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.FIX)
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_fix_then_fix(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` and another ``fix:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='0.0.1-pre',
        version_name='v0.0.1-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='0.0.1-beta',
        version_name='v0.0.1-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='0.0.1',
        version_name='v0.0.1',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.FIX)
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_fix_then_feat(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` and a ``feat:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )
    expected_output_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.FIX)
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_fix_then_breaking(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``fix:`` and a ``feat!:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.FIX)
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_feat_then_chore(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat:`` and a ``chore:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.FEATURE)
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_feat_then_fix(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat:`` and a ``fix:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.FEATURE)
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_feat_then_feat(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat:`` and another ``feat:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )
    expected_output_release = ActionOutputs(
        version='0.1.0-pre',
        version_name='v0.1.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='0.1.0-beta',
        version_name='v0.1.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='0.1.0',
        version_name='v0.1.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.FEATURE)
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_feat_then_breaking(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat:`` and a ``feat!:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.FEATURE)
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_breaking_then_chore(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat!:`` and a ``chore:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.BREAKING_FEATURE)
    repo.commit(CommitMessages.CHORE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_breaking_then_fix(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat!:`` and a ``fix:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.BREAKING_FEATURE)
    repo.commit(CommitMessages.FIX)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_breaking_then_feat(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat!:`` and another ``feat:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )
    expected_output_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.BREAKING_FEATURE)
    repo.commit(CommitMessages.FEATURE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)


def test_breaking_then_breaking(repo: TestRepo) -> None:
    """Test Case: Run the action after a ``feat!:`` and another ``feat!:`` commit."""
    # Arrange
    args_release = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='pre',
        reference_version_suffix=None,
        create_tag=True
    )

    expected_output_release = ActionOutputs(
        version='1.0.0-pre',
        version_name='v1.0.0-pre',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_beta = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix='beta',
        only_bump_suffix=True,
        reference_version_suffix='pre',
        create_tag=True
    )

    expected_output_beta = ActionOutputs(
        version='1.0.0-beta',
        version_name='v1.0.0-beta',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    args_prod = ActionInputs(
        git_username='wemogy IT',
        git_email='it@wemogy.com',
        prefix='v',
        suffix=None,
        only_bump_suffix=True,
        reference_version_suffix='beta',
        create_tag=True
    )

    expected_output_prod = ActionOutputs(
        version='1.0.0',
        version_name='v1.0.0',
        previous_version='',
        previous_version_name='',
        tag_created=True
    )

    # Act
    repo.commit(CommitMessages.BREAKING_FEATURE)
    repo.commit(CommitMessages.BREAKING_FEATURE)

    repo.merge('main', 'release')
    actual_output_release = run_action(args_release)
    tag_release = repo.get_latest_tag_name()

    repo.merge('release', 'release-beta')
    actual_output_beta = run_action(args_beta)
    tag_beta = repo.get_latest_tag_name()

    repo.merge('release-beta', 'release-prod')
    actual_output_prod = run_action(args_prod)
    tag_prod = repo.get_latest_tag_name()

    # Assert
    assert_that(actual_output_release).is_equal_to(expected_output_release)
    assert_that(tag_release).is_equal_to(expected_output_release.version_name)

    assert_that(actual_output_beta).is_equal_to(expected_output_beta)
    assert_that(tag_beta).is_equal_to(expected_output_beta.version_name)

    assert_that(actual_output_prod).is_equal_to(expected_output_prod)
    assert_that(tag_prod).is_equal_to(expected_output_prod.version_name)
