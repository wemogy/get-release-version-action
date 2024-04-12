"""Test all scenarios where one hotfix / cherrypick is made."""
# pylint: disable=too-many-locals,too-many-lines,duplicate-code
import unittest
from unittest import TestCase

from utils import ActionInputs, ActionOutputs, CommitMessages, TestRepo, run_action, setup_logging


class OneHotfixTestCase(TestCase):
    """Test all scenarios where one hotfix / cherrypick is made."""
    repo: TestRepo

    @classmethod
    def setUpClass(cls) -> None:
        setup_logging()

    def setUp(self) -> None:
        self.repo = TestRepo()

    def tearDown(self) -> None:
        self.repo.close()

    def test_fix_then_hotfix(self) -> None:
        """Test Case: Run the action after a ``fix:`` commit and after a hotfix."""
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

        # Hotfix
        args_hotfix_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
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
            previous_version_suffix='pre',
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
            suffix='',
            previous_version_suffix='beta',
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

        # Hotfix
        self.repo.checkout('main')
        commit = self.repo.commit(CommitMessages.FIX)

        self.repo.cherrypick(commit, 'release')
        actual_output_hotfix_release = run_action(args_hotfix_release)
        tag_hotfix_release = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-beta')
        actual_output_hotfix_beta = run_action(args_hotfix_beta)
        tag_hotfix_beta = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-prod')
        actual_output_hotfix_prod = run_action(args_hotfix_prod)
        tag_hotfix_prod = self.repo.get_latest_tag_name()

        # Assert
        # Fix
        self.assertEqual(expected_output_fix_release, actual_output_fix_release)
        self.assertEqual(expected_output_fix_release.version_name, tag_fix_release)

        self.assertEqual(expected_output_fix_beta, actual_output_fix_beta)
        self.assertEqual(expected_output_fix_beta.version_name, tag_fix_beta)

        self.assertEqual(expected_output_fix_prod, actual_output_fix_prod)
        self.assertEqual(expected_output_fix_prod.version_name, tag_fix_prod)

        # Hotfix
        self.assertEqual(expected_output_hotfix_release, actual_output_hotfix_release)
        self.assertEqual(expected_output_hotfix_release.version_name, tag_hotfix_release)

        self.assertEqual(expected_output_hotfix_beta, actual_output_hotfix_beta)
        self.assertEqual(expected_output_hotfix_beta.version_name, tag_hotfix_beta)

        self.assertEqual(expected_output_hotfix_prod, actual_output_hotfix_prod)
        self.assertEqual(expected_output_hotfix_prod.version_name, tag_hotfix_prod)

    def test_feature_then_hotfix(self) -> None:
        """Test Case: Run the action after a ``feat:`` commit and after a hotfix."""
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

        # Hotfix
        args_hotfix_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
            bumping_suffix='hotfix',
            only_bump_suffix=True,
            create_tag=True
        )

        expected_output_hotfix_release = ActionOutputs(
            version='0.1.0-pre-hotfix.1',
            version_name='v0.1.0-pre-hotfix.1',
            previous_version='0.1.0-pre',
            previous_version_name='v0.1.0-pre',
            tag_created=True
        )

        args_hotfix_beta = ActionInputs(
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
            bumping_suffix='hotfix',
            only_bump_suffix=True,
            create_tag=True
        )

        expected_output_hotfix_beta = ActionOutputs(
            version='0.1.0-beta-hotfix.1',
            version_name='v0.1.0-beta-hotfix.1',
            previous_version='0.1.0-beta',
            previous_version_name='v0.1.0-beta',
            tag_created=True
        )

        args_hotfix_prod = ActionInputs(
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
            bumping_suffix='hotfix',
            only_bump_suffix=True,
            create_tag=True
        )

        expected_output_hotfix_prod = ActionOutputs(
            version='0.1.0-hotfix.1',
            version_name='v0.1.0-hotfix.1',
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

        # Hotfix
        self.repo.checkout('main')
        commit = self.repo.commit(CommitMessages.FIX)

        self.repo.cherrypick(commit, 'release')
        actual_output_hotfix_release = run_action(args_hotfix_release)
        tag_hotfix_release = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-beta')
        actual_output_hotfix_beta = run_action(args_hotfix_beta)
        tag_hotfix_beta = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-prod')
        actual_output_hotfix_prod = run_action(args_hotfix_prod)
        tag_hotfix_prod = self.repo.get_latest_tag_name()

        # Assert
        # Feature
        self.assertEqual(expected_output_feat_release, actual_output_feat_release)
        self.assertEqual(expected_output_feat_release.version_name, tag_feat_release)

        self.assertEqual(expected_output_feat_beta, actual_output_feat_beta)
        self.assertEqual(expected_output_feat_beta.version_name, tag_feat_beta)

        self.assertEqual(expected_output_feat_prod, actual_output_feat_prod)
        self.assertEqual(expected_output_feat_prod.version_name, tag_feat_prod)

        # Hotfix
        self.assertEqual(expected_output_hotfix_release, actual_output_hotfix_release)
        self.assertEqual(expected_output_hotfix_release.version_name, tag_hotfix_release)

        self.assertEqual(expected_output_hotfix_beta, actual_output_hotfix_beta)
        self.assertEqual(expected_output_hotfix_beta.version_name, tag_hotfix_beta)

        self.assertEqual(expected_output_hotfix_prod, actual_output_hotfix_prod)
        self.assertEqual(expected_output_hotfix_prod.version_name, tag_hotfix_prod)

    def test_breaking_then_hotfix(self) -> None:
        """Test Case: Run the action after a ``feat!:`` commit and after a hotfix."""
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

        # Hotfix
        args_hotfix_release = ActionInputs(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
            bumping_suffix='hotfix',
            only_bump_suffix=True,
            create_tag=True
        )

        expected_output_hotfix_release = ActionOutputs(
            version='1.0.0-pre-hotfix.1',
            version_name='v1.0.0-pre-hotfix.1',
            previous_version='1.0.0-pre',
            previous_version_name='v1.0.0-pre',
            tag_created=True
        )

        args_hotfix_beta = ActionInputs(
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
            bumping_suffix='hotfix',
            only_bump_suffix=True,
            create_tag=True
        )

        expected_output_hotfix_beta = ActionOutputs(
            version='1.0.0-beta-hotfix.1',
            version_name='v1.0.0-beta-hotfix.1',
            previous_version='1.0.0-beta',
            previous_version_name='v1.0.0-beta',
            tag_created=True
        )

        args_hotfix_prod = ActionInputs(
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
            bumping_suffix='hotfix',
            only_bump_suffix=True,
            create_tag=True
        )

        expected_output_hotfix_prod = ActionOutputs(
            version='1.0.0-hotfix.1',
            version_name='v1.0.0-hotfix.1',
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

        # Hotfix
        self.repo.checkout('main')
        commit = self.repo.commit(CommitMessages.FIX)

        self.repo.cherrypick(commit, 'release')
        actual_output_hotfix_release = run_action(args_hotfix_release)
        tag_hotfix_release = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-beta')
        actual_output_hotfix_beta = run_action(args_hotfix_beta)
        tag_hotfix_beta = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-prod')
        actual_output_hotfix_prod = run_action(args_hotfix_prod)
        tag_hotfix_prod = self.repo.get_latest_tag_name()

        # Assert
        # Breaking
        self.assertEqual(expected_output_breaking_release, actual_output_breaking_release)
        self.assertEqual(expected_output_breaking_release.version_name, tag_breaking_release)

        self.assertEqual(expected_output_breaking_beta, actual_output_breaking_beta)
        self.assertEqual(expected_output_breaking_beta.version_name, tag_breaking_beta)

        self.assertEqual(expected_output_breaking_prod, actual_output_breaking_prod)
        self.assertEqual(expected_output_breaking_prod.version_name, tag_breaking_prod)

        # Hotfix
        self.assertEqual(expected_output_hotfix_release, actual_output_hotfix_release)
        self.assertEqual(expected_output_hotfix_release.version_name, tag_hotfix_release)

        self.assertEqual(expected_output_hotfix_beta, actual_output_hotfix_beta)
        self.assertEqual(expected_output_hotfix_beta.version_name, tag_hotfix_beta)

        self.assertEqual(expected_output_hotfix_prod, actual_output_hotfix_prod)
        self.assertEqual(expected_output_hotfix_prod.version_name, tag_hotfix_prod)


if __name__ == '__main__':
    unittest.main()
