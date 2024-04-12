"""Test all scenarios where two commits with a release after each are made."""
# pylint: disable=too-many-locals,too-many-lines,duplicate-code
import unittest
from unittest import TestCase

from utils import ActionInputs, ActionOutputs, CommitMessages, TestRepo, run_action, setup_logging


class TwoVersionTestCase(TestCase):
    """Test all scenarios where two commits with a release after each are made."""
    repo: TestRepo

    @classmethod
    def setUpClass(cls) -> None:
        setup_logging()

    def setUp(self) -> None:
        self.repo = TestRepo()

    def tearDown(self) -> None:
        self.repo.close()

    def test_chore_then_chore(self) -> None:
        """Test Case: Run the action after a ``chore:`` and another ``chore:`` commit."""
        # Arrange
        # Chore 1
        args_chore1_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.CHORE)

        self.repo.merge('main', 'release')
        actual_output_chore1_release = run_action(args_chore1_release)
        tag_chore1_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_chore1_beta = run_action(args_chore1_beta)
        tag_chore1_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_chore1_prod = run_action(args_chore1_prod)
        tag_chore1_prod = self.repo.get_latest_tag_name()

        # Chore 2
        self.repo.commit(CommitMessages.CHORE)

        self.repo.merge('main', 'release')
        actual_output_chore2_release = run_action(args_chore2_release)
        tag_chore2_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_chore2_beta = run_action(args_chore2_beta)
        tag_chore2_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_chore2_prod = run_action(args_chore2_prod)
        tag_chore2_prod = self.repo.get_latest_tag_name()

        # Assert
        # Chore 1
        self.assertEqual(expected_output_chore1_release, actual_output_chore1_release)
        self.assertEqual(None, tag_chore1_release)

        self.assertEqual(expected_output_chore1_beta, actual_output_chore1_beta)
        self.assertEqual(None, tag_chore1_beta)

        self.assertEqual(expected_output_chore1_prod, actual_output_chore1_prod)
        self.assertEqual(None, tag_chore1_prod)

        # Chore 2
        self.assertEqual(expected_output_chore2_release, actual_output_chore2_release)
        self.assertEqual(None, tag_chore2_release)

        self.assertEqual(expected_output_chore2_beta, actual_output_chore2_beta)
        self.assertEqual(None, tag_chore2_beta)

        self.assertEqual(expected_output_chore2_prod, actual_output_chore2_prod)
        self.assertEqual(None, tag_chore2_prod)

    def test_chore_then_fix(self) -> None:
        """Test Case: Run the action after a ``chore:`` and a ``fix:`` commit."""
        # Arrange
        # Chore
        args_chore_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            previous_version_suffix='pre',
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
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.CHORE)

        self.repo.merge('main', 'release')
        actual_output_chore_release = run_action(args_chore_release)
        tag_chore_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_chore_beta = run_action(args_chore_beta)
        tag_chore_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_chore_prod = run_action(args_chore_prod)
        tag_chore_prod = self.repo.get_latest_tag_name()

        # Fix
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_fix_release = run_action(args_fix_release)
        tag_fix_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_fix_beta = run_action(args_fix_beta)
        tag_fix_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_fix_prod = run_action(args_fix_prod)
        tag_fix_prod = self.repo.get_latest_tag_name()

        # Assert
        # Chore
        self.assertEqual(expected_output_chore_release, actual_output_chore_release)
        self.assertEqual(None, tag_chore_release)

        self.assertEqual(expected_output_chore_beta, actual_output_chore_beta)
        self.assertEqual(None, tag_chore_beta)

        self.assertEqual(expected_output_chore_prod, actual_output_chore_prod)
        self.assertEqual(None, tag_chore_prod)

        # Fix
        self.assertEqual(expected_output_fix_release, actual_output_fix_release)
        self.assertEqual(expected_output_fix_release.version_name, tag_fix_release)

        self.assertEqual(expected_output_fix_beta, actual_output_fix_beta)
        self.assertEqual(expected_output_fix_beta.version_name, tag_fix_beta)

        self.assertEqual(expected_output_fix_prod, actual_output_fix_prod)
        self.assertEqual(expected_output_fix_prod.version_name, tag_fix_prod)

    def test_chore_then_feat(self) -> None:
        """Test Case: Run the action after a ``chore:`` and a ``feat:`` commit."""
        # Arrange
        # Chore
        args_chore_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.CHORE)

        self.repo.merge('main', 'release')
        actual_output_chore_release = run_action(args_chore_release)
        tag_chore_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_chore_beta = run_action(args_chore_beta)
        tag_chore_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_chore_prod = run_action(args_chore_prod)
        tag_chore_prod = self.repo.get_latest_tag_name()

        # Feature
        self.repo.commit(CommitMessages.FEATURE)

        self.repo.merge('main', 'release')
        actual_output_feat_release = run_action(args_feat_release)
        tag_feat_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_feat_beta = run_action(args_feat_beta)
        tag_feat_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_feat_prod = run_action(args_feat_prod)
        tag_feat_prod = self.repo.get_latest_tag_name()

        # Assert
        # Chore
        self.assertEqual(expected_output_chore_release, actual_output_chore_release)
        self.assertEqual(None, tag_chore_release)

        self.assertEqual(expected_output_chore_beta, actual_output_chore_beta)
        self.assertEqual(None, tag_chore_beta)

        self.assertEqual(expected_output_chore_prod, actual_output_chore_prod)
        self.assertEqual(None, tag_chore_prod)

        # Feature
        self.assertEqual(expected_output_feat_release, actual_output_feat_release)
        self.assertEqual(None, tag_feat_release)

        self.assertEqual(expected_output_feat_beta, actual_output_feat_beta)
        self.assertEqual(None, tag_feat_beta)

        self.assertEqual(expected_output_feat_prod, actual_output_feat_prod)
        self.assertEqual(None, tag_feat_prod)

    def test_chore_then_breaking(self) -> None:
        """Test Case: Run the action after a ``chore:`` and a ``feat!:`` commit."""
        # Arrange
        # Chore
        args_chore_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.CHORE)

        self.repo.merge('main', 'release')
        actual_output_chore_release = run_action(args_chore_release)
        tag_chore_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_chore_beta = run_action(args_chore_beta)
        tag_chore_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_chore_prod = run_action(args_chore_prod)
        tag_chore_prod = self.repo.get_latest_tag_name()

        # Breaking
        self.repo.commit(CommitMessages.BREAKING_FEATURE)

        self.repo.merge('main', 'release')
        actual_output_breaking_release = run_action(args_breaking_release)
        tag_breaking_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_breaking_beta = run_action(args_breaking_beta)
        tag_breaking_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_breaking_prod = run_action(args_breaking_prod)
        tag_breaking_prod = self.repo.get_latest_tag_name()

        # Assert
        # Chore
        self.assertEqual(expected_output_chore_release, actual_output_chore_release)
        self.assertEqual(None, tag_chore_release)

        self.assertEqual(expected_output_chore_beta, actual_output_chore_beta)
        self.assertEqual(None, tag_chore_beta)

        self.assertEqual(expected_output_chore_prod, actual_output_chore_prod)
        self.assertEqual(None, tag_chore_prod)

        # Breaking
        self.assertEqual(expected_output_breaking_release, actual_output_breaking_release)
        self.assertEqual(expected_output_breaking_release.version_name, tag_breaking_release)

        self.assertEqual(expected_output_breaking_beta, actual_output_breaking_beta)
        self.assertEqual(expected_output_breaking_beta.version_name, tag_breaking_beta)

        self.assertEqual(expected_output_breaking_prod, actual_output_breaking_prod)
        self.assertEqual(expected_output_breaking_prod.version_name, tag_breaking_prod)

    def test_fix_then_chore(self) -> None:
        """Test Case: Run the action after a ``fix:`` and a ``chore:`` commit."""
        # Arrange
        # Fix
        args_fix_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            previous_version_suffix='pre',
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
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_chore_release = ActionOutputs(
            version='0.0.1-pre',
            version_name='v0.0.1-pre',
            previous_version='',
            previous_version_name='',
            tag_created=False
        )

        args_chore_beta = ActionInputs(
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_chore_beta = ActionOutputs(
            version='0.0.1-beta',
            version_name='v0.0.1-beta',
            previous_version='',
            previous_version_name='',
            tag_created=False
        )

        args_chore_prod = ActionInputs(
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
            create_tag=True
        )

        expected_output_chore_prod = ActionOutputs(
            version='0.0.1',
            version_name='v0.0.1',
            previous_version='',
            previous_version_name='',
            tag_created=False
        )

        # Act
        # Fix
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_fix_release = run_action(args_fix_release)
        tag_fix_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_fix_beta = run_action(args_fix_beta)
        tag_fix_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_fix_prod = run_action(args_fix_prod)
        tag_fix_prod = self.repo.get_latest_tag_name()

        # Chore
        self.repo.commit(CommitMessages.CHORE)

        self.repo.merge('main', 'release')
        actual_output_chore_release = run_action(args_chore_release)
        tag_chore_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_chore_beta = run_action(args_chore_beta)
        tag_chore_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_chore_prod = run_action(args_chore_prod)
        tag_chore_prod = self.repo.get_latest_tag_name()

        # Assert
        # Fix
        self.assertEqual(expected_output_fix_release, actual_output_fix_release)
        self.assertEqual(expected_output_fix_release.version_name, tag_fix_release)

        self.assertEqual(expected_output_fix_beta, actual_output_fix_beta)
        self.assertEqual(expected_output_fix_beta.version_name, tag_fix_beta)

        self.assertEqual(expected_output_fix_prod, actual_output_fix_prod)
        self.assertEqual(expected_output_fix_prod.version_name, tag_fix_prod)

        # Chore
        self.assertEqual(expected_output_chore_release, actual_output_chore_release)
        self.assertEqual(expected_output_fix_release.version_name, tag_chore_release)

        self.assertEqual(expected_output_chore_beta, actual_output_chore_beta)
        self.assertEqual(expected_output_fix_beta.version_name, tag_chore_beta)

        self.assertEqual(expected_output_chore_prod, actual_output_chore_prod)
        self.assertEqual(expected_output_fix_prod.version_name, tag_chore_prod)

    def test_fix_then_fix(self) -> None:
        """Test Case: Run the action after a ``fix:`` and another ``fix:`` commit."""
        # Arrange
        # Fix 1
        args_fix1_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            previous_version_suffix='pre',
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
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_fix1_release = run_action(args_fix1_release)
        tag_fix1_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_fix1_beta = run_action(args_fix1_beta)
        tag_fix1_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_fix1_prod = run_action(args_fix1_prod)
        tag_fix1_prod = self.repo.get_latest_tag_name()

        # Fix 2
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_fix2_release = run_action(args_fix2_release)
        tag_fix2_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_fix2_beta = run_action(args_fix2_beta)
        tag_fix2_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_fix2_prod = run_action(args_fix2_prod)
        tag_fix2_prod = self.repo.get_latest_tag_name()

        # Assert
        # Fix 1
        self.assertEqual(expected_output_fix1_release, actual_output_fix1_release)
        self.assertEqual(expected_output_fix1_release.version_name, tag_fix1_release)

        self.assertEqual(expected_output_fix1_beta, actual_output_fix1_beta)
        self.assertEqual(expected_output_fix1_beta.version_name, tag_fix1_beta)

        self.assertEqual(expected_output_fix1_prod, actual_output_fix1_prod)
        self.assertEqual(expected_output_fix1_prod.version_name, tag_fix1_prod)

        # Fix 2
        self.assertEqual(expected_output_fix2_release, actual_output_fix2_release)
        self.assertEqual(expected_output_fix2_release.version_name, tag_fix2_release)

        self.assertEqual(expected_output_fix2_beta, actual_output_fix2_beta)
        self.assertEqual(expected_output_fix2_beta.version_name, tag_fix2_beta)

        self.assertEqual(expected_output_fix2_prod, actual_output_fix2_prod)
        self.assertEqual(expected_output_fix2_prod.version_name, tag_fix2_prod)

    def test_fix_then_feat(self) -> None:
        """Test Case: Run the action after a ``fix:`` and a ``feat:`` commit."""
        # Arrange
        # Fix
        args_fix_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            previous_version_suffix='pre',
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
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_fix_release = run_action(args_fix_release)
        tag_fix_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_fix_beta = run_action(args_fix_beta)
        tag_fix_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_fix_prod = run_action(args_fix_prod)
        tag_fix_prod = self.repo.get_latest_tag_name()

        # Feature
        self.repo.commit(CommitMessages.FEATURE)

        self.repo.merge('main', 'release')
        actual_output_feat_release = run_action(args_feat_release)
        tag_feat_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_feat_beta = run_action(args_feat_beta)
        tag_feat_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_feat_prod = run_action(args_feat_prod)
        tag_feat_prod = self.repo.get_latest_tag_name()

        # Assert
        # Fix
        self.assertEqual(expected_output_fix_release, actual_output_fix_release)
        self.assertEqual(expected_output_fix_release.version_name, tag_fix_release)

        self.assertEqual(expected_output_fix_beta, actual_output_fix_beta)
        self.assertEqual(expected_output_fix_beta.version_name, tag_fix_beta)

        self.assertEqual(expected_output_fix_prod, actual_output_fix_prod)
        self.assertEqual(expected_output_fix_prod.version_name, tag_fix_prod)

        # Feature
        self.assertEqual(expected_output_feat_release, actual_output_feat_release)
        self.assertEqual(expected_output_feat_release.version_name, tag_feat_release)

        self.assertEqual(expected_output_feat_beta, actual_output_feat_beta)
        self.assertEqual(expected_output_feat_beta.version_name, tag_feat_beta)

        self.assertEqual(expected_output_feat_prod, actual_output_feat_prod)
        self.assertEqual(expected_output_feat_prod.version_name, tag_feat_prod)

    def test_fix_then_breaking(self) -> None:
        """Test Case: Run the action after a ``fix:`` and a ``feat!:`` commit."""
        # Arrange
        # Fix
        args_fix_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            previous_version_suffix='pre',
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
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_fix_release = run_action(args_fix_release)
        tag_fix_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_fix_beta = run_action(args_fix_beta)
        tag_fix_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_fix_prod = run_action(args_fix_prod)
        tag_fix_prod = self.repo.get_latest_tag_name()

        # Breaking
        self.repo.commit(CommitMessages.BREAKING_FEATURE)

        self.repo.merge('main', 'release')
        actual_output_breaking_release = run_action(args_breaking_release)
        tag_breaking_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_breaking_beta = run_action(args_breaking_beta)
        tag_breaking_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_breaking_prod = run_action(args_breaking_prod)
        tag_breaking_prod = self.repo.get_latest_tag_name()

        # Assert
        # Fix
        self.assertEqual(expected_output_fix_release, actual_output_fix_release)
        self.assertEqual(expected_output_fix_release.version_name, tag_fix_release)

        self.assertEqual(expected_output_fix_beta, actual_output_fix_beta)
        self.assertEqual(expected_output_fix_beta.version_name, tag_fix_beta)

        self.assertEqual(expected_output_fix_prod, actual_output_fix_prod)
        self.assertEqual(expected_output_fix_prod.version_name, tag_fix_prod)

        # Breaking
        self.assertEqual(expected_output_breaking_release, actual_output_breaking_release)
        self.assertEqual(expected_output_breaking_release.version_name, tag_breaking_release)

        self.assertEqual(expected_output_breaking_beta, actual_output_breaking_beta)
        self.assertEqual(expected_output_breaking_beta.version_name, tag_breaking_beta)

        self.assertEqual(expected_output_breaking_prod, actual_output_breaking_prod)
        self.assertEqual(expected_output_breaking_prod.version_name, tag_breaking_prod)

    def test_feat_then_chore(self) -> None:
        """Test Case: Run the action after a ``feat:`` and a ``chore:`` commit."""
        # Arrange
        # Feature
        args_feat_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_chore_release = ActionOutputs(
            version='0.1.0-pre',
            version_name='v0.1.0-pre',
            previous_version='',
            previous_version_name='',
            tag_created=False
        )

        args_chore_beta = ActionInputs(
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_chore_beta = ActionOutputs(
            version='0.1.0-beta',
            version_name='v0.1.0-beta',
            previous_version='',
            previous_version_name='',
            tag_created=False
        )

        args_chore_prod = ActionInputs(
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
            create_tag=True
        )

        expected_output_chore_prod = ActionOutputs(
            version='0.1.0',
            version_name='v0.1.0',
            previous_version='',
            previous_version_name='',
            tag_created=False
        )

        # Act
        # Feature
        self.repo.commit(CommitMessages.FEATURE)

        self.repo.merge('main', 'release')
        actual_output_feat_release = run_action(args_feat_release)
        tag_feat_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_feat_beta = run_action(args_feat_beta)
        tag_feat_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_feat_prod = run_action(args_feat_prod)
        tag_feat_prod = self.repo.get_latest_tag_name()

        # Chore
        self.repo.commit(CommitMessages.CHORE)

        self.repo.merge('main', 'release')
        actual_output_chore_release = run_action(args_chore_release)
        tag_chore_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_chore_beta = run_action(args_chore_beta)
        tag_chore_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_chore_prod = run_action(args_chore_prod)
        tag_chore_prod = self.repo.get_latest_tag_name()

        # Assert
        # Feature
        self.assertEqual(expected_output_feat_release, actual_output_feat_release)
        self.assertEqual(expected_output_feat_release.version_name, tag_feat_release)

        self.assertEqual(expected_output_feat_beta, actual_output_feat_beta)
        self.assertEqual(expected_output_feat_beta.version_name, tag_feat_beta)

        self.assertEqual(expected_output_feat_prod, actual_output_feat_prod)
        self.assertEqual(expected_output_feat_prod.version_name, tag_feat_prod)

        # Chore
        self.assertEqual(expected_output_chore_release, actual_output_chore_release)
        self.assertEqual(expected_output_feat_release.version_name, tag_chore_release)

        self.assertEqual(expected_output_chore_beta, actual_output_chore_beta)
        self.assertEqual(expected_output_feat_beta.version_name, tag_chore_beta)

        self.assertEqual(expected_output_chore_prod, actual_output_chore_prod)
        self.assertEqual(expected_output_feat_prod.version_name, tag_chore_prod)

    def test_feat_then_fix(self) -> None:
        """Test Case: Run the action after a ``feat:`` and a ``fix:`` commit."""
        # Arrange
        # Feature
        args_feat_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.FEATURE)

        self.repo.merge('main', 'release')
        actual_output_feat_release = run_action(args_feat_release)
        tag_feat_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_feat_beta = run_action(args_feat_beta)
        tag_feat_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_feat_prod = run_action(args_feat_prod)
        tag_feat_prod = self.repo.get_latest_tag_name()

        # Fix
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_fix_release = run_action(args_fix_release)
        tag_fix_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_fix_beta = run_action(args_fix_beta)
        tag_fix_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_fix_prod = run_action(args_fix_prod)
        tag_fix_prod = self.repo.get_latest_tag_name()

        # Assert
        # Feature
        self.assertEqual(expected_output_feat_release, actual_output_feat_release)
        self.assertEqual(expected_output_feat_release.version_name, tag_feat_release)

        self.assertEqual(expected_output_feat_beta, actual_output_feat_beta)
        self.assertEqual(expected_output_feat_beta.version_name, tag_feat_beta)

        self.assertEqual(expected_output_feat_prod, actual_output_feat_prod)
        self.assertEqual(expected_output_feat_prod.version_name, tag_feat_prod)

        # Fix
        self.assertEqual(expected_output_fix_release, actual_output_fix_release)
        self.assertEqual(expected_output_fix_release.version_name, tag_fix_release)

        self.assertEqual(expected_output_fix_beta, actual_output_fix_beta)
        self.assertEqual(expected_output_fix_beta.version_name, tag_fix_beta)

        self.assertEqual(expected_output_fix_prod, actual_output_fix_prod)
        self.assertEqual(expected_output_fix_prod.version_name, tag_fix_prod)

    def test_feat_then_feat(self) -> None:
        """Test Case: Run the action after a ``feat:`` and another ``feat:`` commit."""
        # Arrange
        # Feature 1
        args_feat1_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.FEATURE)

        self.repo.merge('main', 'release')
        actual_output_feat1_release = run_action(args_feat1_release)
        tag_feat1_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_feat1_beta = run_action(args_feat1_beta)
        tag_feat1_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_feat1_prod = run_action(args_feat1_prod)
        tag_feat1_prod = self.repo.get_latest_tag_name()

        # Feature 2
        self.repo.commit(CommitMessages.FEATURE)

        self.repo.merge('main', 'release')
        actual_output_feat2_release = run_action(args_feat2_release)
        tag_feat2_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_feat2_beta = run_action(args_feat2_beta)
        tag_feat2_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_feat2_prod = run_action(args_feat2_prod)
        tag_feat2_prod = self.repo.get_latest_tag_name()

        # Assert
        # Feature 1
        self.assertEqual(expected_output_feat1_release, actual_output_feat1_release)
        self.assertEqual(expected_output_feat1_release.version_name, tag_feat1_release)

        self.assertEqual(expected_output_feat1_beta, actual_output_feat1_beta)
        self.assertEqual(expected_output_feat1_beta.version_name, tag_feat1_beta)

        self.assertEqual(expected_output_feat1_prod, actual_output_feat1_prod)
        self.assertEqual(expected_output_feat1_prod.version_name, tag_feat1_prod)

        # Feature 2
        self.assertEqual(expected_output_feat2_release, actual_output_feat2_release)
        self.assertEqual(expected_output_feat2_release.version_name, tag_feat2_release)

        self.assertEqual(expected_output_feat2_beta, actual_output_feat2_beta)
        self.assertEqual(expected_output_feat2_beta.version_name, tag_feat2_beta)

        self.assertEqual(expected_output_feat2_prod, actual_output_feat2_prod)
        self.assertEqual(expected_output_feat2_prod.version_name, tag_feat2_prod)

    def test_feat_then_breaking(self) -> None:
        """Test Case: Run the action after a ``feat:`` and a ``feat!:`` commit."""
        # Arrange
        # Feature
        args_feat_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.FEATURE)

        self.repo.merge('main', 'release')
        actual_output_feat_release = run_action(args_feat_release)
        tag_feat_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_feat_beta = run_action(args_feat_beta)
        tag_feat_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_feat_prod = run_action(args_feat_prod)
        tag_feat_prod = self.repo.get_latest_tag_name()

        # Breaking
        self.repo.commit(CommitMessages.BREAKING_FEATURE)

        self.repo.merge('main', 'release')
        actual_output_breaking_release = run_action(args_breaking_release)
        tag_breaking_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_breaking_beta = run_action(args_breaking_beta)
        tag_breaking_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_breaking_prod = run_action(args_breaking_prod)
        tag_breaking_prod = self.repo.get_latest_tag_name()

        # Assert
        # Feature
        self.assertEqual(expected_output_feat_release, actual_output_feat_release)
        self.assertEqual(expected_output_feat_release.version_name, tag_feat_release)

        self.assertEqual(expected_output_feat_beta, actual_output_feat_beta)
        self.assertEqual(expected_output_feat_beta.version_name, tag_feat_beta)

        self.assertEqual(expected_output_feat_prod, actual_output_feat_prod)
        self.assertEqual(expected_output_feat_prod.version_name, tag_feat_prod)

        # Breaking
        self.assertEqual(expected_output_breaking_release, actual_output_breaking_release)
        self.assertEqual(expected_output_breaking_release.version_name, tag_breaking_release)

        self.assertEqual(expected_output_breaking_beta, actual_output_breaking_beta)
        self.assertEqual(expected_output_breaking_beta.version_name, tag_breaking_beta)

        self.assertEqual(expected_output_breaking_prod, actual_output_breaking_prod)
        self.assertEqual(expected_output_breaking_prod.version_name, tag_breaking_prod)

    def test_breaking_then_chore(self) -> None:
        """Test Case: Run the action after a ``feat!:`` and a ``chore:`` commit."""
        # Arrange
        # Breaking
        args_breaking_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_chore_release = ActionOutputs(
            version='1.0.0-pre',
            version_name='v1.0.0-pre',
            previous_version='',
            previous_version_name='',
            tag_created=False
        )

        args_chore_beta = ActionInputs(
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_chore_beta = ActionOutputs(
            version='1.0.0-beta',
            version_name='v1.0.0-beta',
            previous_version='',
            previous_version_name='',
            tag_created=False
        )

        args_chore_prod = ActionInputs(
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
            create_tag=True
        )

        expected_output_chore_prod = ActionOutputs(
            version='1.0.0',
            version_name='v1.0.0',
            previous_version='',
            previous_version_name='',
            tag_created=False
        )

        # Act
        # Breaking
        self.repo.commit(CommitMessages.BREAKING_FEATURE)

        self.repo.merge('main', 'release')
        actual_output_breaking_release = run_action(args_breaking_release)
        tag_breaking_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_breaking_beta = run_action(args_breaking_beta)
        tag_breaking_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_breaking_prod = run_action(args_breaking_prod)
        tag_breaking_prod = self.repo.get_latest_tag_name()

        # Chore
        self.repo.commit(CommitMessages.CHORE)

        self.repo.merge('main', 'release')
        actual_output_chore_release = run_action(args_chore_release)
        tag_chore_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_chore_beta = run_action(args_chore_beta)
        tag_chore_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_chore_prod = run_action(args_chore_prod)
        tag_chore_prod = self.repo.get_latest_tag_name()

        # Assert
        # Breaking
        self.assertEqual(expected_output_breaking_release, actual_output_breaking_release)
        self.assertEqual(expected_output_breaking_release.version_name, tag_breaking_release)

        self.assertEqual(expected_output_breaking_beta, actual_output_breaking_beta)
        self.assertEqual(expected_output_breaking_beta.version_name, tag_breaking_beta)

        self.assertEqual(expected_output_breaking_prod, actual_output_breaking_prod)
        self.assertEqual(expected_output_breaking_prod.version_name, tag_breaking_prod)

        # Chore
        self.assertEqual(expected_output_chore_release, actual_output_chore_release)
        self.assertEqual(expected_output_breaking_release.version_name, tag_chore_release)

        self.assertEqual(expected_output_chore_beta, actual_output_chore_beta)
        self.assertEqual(expected_output_breaking_beta.version_name, tag_chore_beta)

        self.assertEqual(expected_output_chore_prod, actual_output_chore_prod)
        self.assertEqual(expected_output_breaking_prod.version_name, tag_chore_prod)

    def test_breaking_then_fix(self) -> None:
        """Test Case: Run the action after a ``feat!:`` and a ``fix:`` commit."""
        # Arrange
        # Breaking
        args_breaking_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.BREAKING_FEATURE)

        self.repo.merge('main', 'release')
        actual_output_breaking_release = run_action(args_breaking_release)
        tag_breaking_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_breaking_beta = run_action(args_breaking_beta)
        tag_breaking_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_breaking_prod = run_action(args_breaking_prod)
        tag_breaking_prod = self.repo.get_latest_tag_name()

        # Fix
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_fix_release = run_action(args_fix_release)
        tag_fix_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_fix_beta = run_action(args_fix_beta)
        tag_fix_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_fix_prod = run_action(args_fix_prod)
        tag_fix_prod = self.repo.get_latest_tag_name()

        # Assert
        # Breaking
        self.assertEqual(expected_output_breaking_release, actual_output_breaking_release)
        self.assertEqual(expected_output_breaking_release.version_name, tag_breaking_release)

        self.assertEqual(expected_output_breaking_beta, actual_output_breaking_beta)
        self.assertEqual(expected_output_breaking_beta.version_name, tag_breaking_beta)

        self.assertEqual(expected_output_breaking_prod, actual_output_breaking_prod)
        self.assertEqual(expected_output_breaking_prod.version_name, tag_breaking_prod)

        # Fix
        self.assertEqual(expected_output_fix_release, actual_output_fix_release)
        self.assertEqual(expected_output_fix_release.version_name, tag_fix_release)

        self.assertEqual(expected_output_fix_beta, actual_output_fix_beta)
        self.assertEqual(expected_output_fix_beta.version_name, tag_fix_beta)

        self.assertEqual(expected_output_fix_prod, actual_output_fix_prod)
        self.assertEqual(expected_output_fix_prod.version_name, tag_fix_prod)

    def test_breaking_then_feat(self) -> None:
        """Test Case: Run the action after a ``feat!:`` and a ``feat:`` commit."""
        # Arrange
        # Breaking
        args_breaking_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.BREAKING_FEATURE)

        self.repo.merge('main', 'release')
        actual_output_breaking_release = run_action(args_breaking_release)
        tag_breaking_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_breaking_beta = run_action(args_breaking_beta)
        tag_breaking_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_breaking_prod = run_action(args_breaking_prod)
        tag_breaking_prod = self.repo.get_latest_tag_name()

        # Feature
        self.repo.commit(CommitMessages.FEATURE)

        self.repo.merge('main', 'release')
        actual_output_feat_release = run_action(args_feat_release)
        tag_feat_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_feat_beta = run_action(args_feat_beta)
        tag_feat_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_feat_prod = run_action(args_feat_prod)
        tag_feat_prod = self.repo.get_latest_tag_name()

        # Assert
        # Breaking
        self.assertEqual(expected_output_breaking_release, actual_output_breaking_release)
        self.assertEqual(expected_output_breaking_release.version_name, tag_breaking_release)

        self.assertEqual(expected_output_breaking_beta, actual_output_breaking_beta)
        self.assertEqual(expected_output_breaking_beta.version_name, tag_breaking_beta)

        self.assertEqual(expected_output_breaking_prod, actual_output_breaking_prod)
        self.assertEqual(expected_output_breaking_prod.version_name, tag_breaking_prod)

        # Feature
        self.assertEqual(expected_output_feat_release, actual_output_feat_release)
        self.assertEqual(expected_output_feat_release.version_name, tag_feat_release)

        self.assertEqual(expected_output_feat_beta, actual_output_feat_beta)
        self.assertEqual(expected_output_feat_beta.version_name, tag_feat_beta)

        self.assertEqual(expected_output_feat_prod, actual_output_feat_prod)
        self.assertEqual(expected_output_feat_prod.version_name, tag_feat_prod)

    def test_breaking_then_breaking(self) -> None:
        """Test Case: Run the action after a ``feat!:`` and another ``feat!:`` commit."""
        # Arrange
        # Breaking 1
        args_breaking1_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
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
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
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
        self.repo.commit(CommitMessages.BREAKING_FEATURE)

        self.repo.merge('main', 'release')
        actual_output_breaking1_release = run_action(args_breaking1_release)
        tag_breaking1_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_breaking1_beta = run_action(args_breaking1_beta)
        tag_breaking1_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_breaking1_prod = run_action(args_breaking1_prod)
        tag_breaking1_prod = self.repo.get_latest_tag_name()

        # Breaking 2
        self.repo.commit(CommitMessages.BREAKING_FEATURE)

        self.repo.merge('main', 'release')
        actual_output_breaking2_release = run_action(args_breaking2_release)
        tag_breaking2_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_breaking2_beta = run_action(args_breaking2_beta)
        tag_breaking2_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_breaking2_prod = run_action(args_breaking2_prod)
        tag_breaking2_prod = self.repo.get_latest_tag_name()

        # Assert
        # Breaking 1
        self.assertEqual(expected_output_breaking1_release, actual_output_breaking1_release)
        self.assertEqual(expected_output_breaking1_release.version_name, tag_breaking1_release)

        self.assertEqual(expected_output_breaking1_beta, actual_output_breaking1_beta)
        self.assertEqual(expected_output_breaking1_beta.version_name, tag_breaking1_beta)

        self.assertEqual(expected_output_breaking1_prod, actual_output_breaking1_prod)
        self.assertEqual(expected_output_breaking1_prod.version_name, tag_breaking1_prod)

        # Breaking 2
        self.assertEqual(expected_output_breaking2_release, actual_output_breaking2_release)
        self.assertEqual(expected_output_breaking2_release.version_name, tag_breaking2_release)

        self.assertEqual(expected_output_breaking2_beta, actual_output_breaking2_beta)
        self.assertEqual(expected_output_breaking2_beta.version_name, tag_breaking2_beta)

        self.assertEqual(expected_output_breaking2_prod, actual_output_breaking2_prod)
        self.assertEqual(expected_output_breaking2_prod.version_name, tag_breaking2_prod)


if __name__ == '__main__':
    unittest.main()
