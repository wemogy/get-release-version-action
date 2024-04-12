"""Test all scenarios where two hotfixes / cherrypicks are made."""
# pylint: disable=too-many-locals,too-many-lines,duplicate-code
import unittest
from unittest import TestCase

from utils import ActionInputs, ActionOutputs, CommitMessages, TestRepo, run_action, setup_logging


class TwoHotfixesTestCase(TestCase):
    """Test all scenarios where two hotfixes / cherrypicks are made."""
    repo: TestRepo

    @classmethod
    def setUpClass(cls) -> None:
        setup_logging()

    def setUp(self) -> None:
        self.repo = TestRepo()

    def tearDown(self) -> None:
        self.repo.close()

    def test_fix_then_hotfixes(self) -> None:
        """Test Case: Run the action after a ``fix:`` commit and after two hotfixes."""
        # Arrange
        # Fix
        args_fix_release = ActionInputs(
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            suffix='',
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
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='',
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
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='',
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

        # Hotfix 1
        self.repo.checkout('main')
        commit = self.repo.commit(CommitMessages.FIX)

        self.repo.cherrypick(commit, 'release')
        actual_output_hotfix1_release = run_action(args_hotfix1_release)
        tag_hotfix1_release = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-beta')
        actual_output_hotfix1_beta = run_action(args_hotfix1_beta)
        tag_hotfix1_beta = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-prod')
        actual_output_hotfix1_prod = run_action(args_hotfix1_prod)
        tag_hotfix1_prod = self.repo.get_latest_tag_name()

        # Hotfix 2
        self.repo.checkout('main')
        commit = self.repo.commit(CommitMessages.FIX)

        self.repo.cherrypick(commit, 'release')
        actual_output_hotfix2_release = run_action(args_hotfix2_release)
        tag_hotfix2_release = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-beta')
        actual_output_hotfix2_beta = run_action(args_hotfix2_beta)
        tag_hotfix2_beta = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-prod')
        actual_output_hotfix2_prod = run_action(args_hotfix2_prod)
        tag_hotfix2_prod = self.repo.get_latest_tag_name()

        # Assert
        # Fix
        self.assertEqual(expected_output_fix_release, actual_output_fix_release)
        self.assertEqual(expected_output_fix_release.version_name, tag_fix_release)

        self.assertEqual(expected_output_fix_beta, actual_output_fix_beta)
        self.assertEqual(expected_output_fix_beta.version_name, tag_fix_beta)

        self.assertEqual(expected_output_fix_prod, actual_output_fix_prod)
        self.assertEqual(expected_output_fix_prod.version_name, tag_fix_prod)

        # Hotfix 1
        self.assertEqual(expected_output_hotfix1_release, actual_output_hotfix1_release)
        self.assertEqual(expected_output_hotfix1_release.version_name, tag_hotfix1_release)

        self.assertEqual(expected_output_hotfix1_beta, actual_output_hotfix1_beta)
        self.assertEqual(expected_output_hotfix1_beta.version_name, tag_hotfix1_beta)

        self.assertEqual(expected_output_hotfix1_prod, actual_output_hotfix1_prod)
        self.assertEqual(expected_output_hotfix1_prod.version_name, tag_hotfix1_prod)

        # Hotfix 2
        self.assertEqual(expected_output_hotfix2_release, actual_output_hotfix2_release)
        self.assertEqual(expected_output_hotfix2_release.version_name, tag_hotfix2_release)

        self.assertEqual(expected_output_hotfix2_beta, actual_output_hotfix2_beta)
        self.assertEqual(expected_output_hotfix2_beta.version_name, tag_hotfix2_beta)

        self.assertEqual(expected_output_hotfix2_prod, actual_output_hotfix2_prod)
        self.assertEqual(expected_output_hotfix2_prod.version_name, tag_hotfix2_prod)

    def test_feat_then_hotfixes(self) -> None:
        """Test Case: Run the action after a ``feat:`` commit and after two hotfixes."""
        # Arrange
        # Feature
        args_feat_release = ActionInputs(
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='',
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
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='',
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
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='',
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
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_feat_release = run_action(args_feat_release)
        tag_feat_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_feat_beta = run_action(args_feat_beta)
        tag_feat_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_feat_prod = run_action(args_feat_prod)
        tag_feat_prod = self.repo.get_latest_tag_name()

        # Hotfix 1
        self.repo.checkout('main')
        commit = self.repo.commit(CommitMessages.FIX)

        self.repo.cherrypick(commit, 'release')
        actual_output_hotfix1_release = run_action(args_hotfix1_release)
        tag_hotfix1_release = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-beta')
        actual_output_hotfix1_beta = run_action(args_hotfix1_beta)
        tag_hotfix1_beta = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-prod')
        actual_output_hotfix1_prod = run_action(args_hotfix1_prod)
        tag_hotfix1_prod = self.repo.get_latest_tag_name()

        # Hotfix 2
        self.repo.checkout('main')
        commit = self.repo.commit(CommitMessages.FIX)

        self.repo.cherrypick(commit, 'release')
        actual_output_hotfix2_release = run_action(args_hotfix2_release)
        tag_hotfix2_release = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-beta')
        actual_output_hotfix2_beta = run_action(args_hotfix2_beta)
        tag_hotfix2_beta = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-prod')
        actual_output_hotfix2_prod = run_action(args_hotfix2_prod)
        tag_hotfix2_prod = self.repo.get_latest_tag_name()

        # Assert
        # Feature
        self.assertEqual(expected_output_feat_release, actual_output_feat_release)
        self.assertEqual(expected_output_feat_release.version_name, tag_feat_release)

        self.assertEqual(expected_output_feat_beta, actual_output_feat_beta)
        self.assertEqual(expected_output_feat_beta.version_name, tag_feat_beta)

        self.assertEqual(expected_output_feat_prod, actual_output_feat_prod)
        self.assertEqual(expected_output_feat_prod.version_name, tag_feat_prod)

        # Hotfix 1
        self.assertEqual(expected_output_hotfix1_release, actual_output_hotfix1_release)
        self.assertEqual(expected_output_hotfix1_release.version_name, tag_hotfix1_release)

        self.assertEqual(expected_output_hotfix1_beta, actual_output_hotfix1_beta)
        self.assertEqual(expected_output_hotfix1_beta.version_name, tag_hotfix1_beta)

        self.assertEqual(expected_output_hotfix1_prod, actual_output_hotfix1_prod)
        self.assertEqual(expected_output_hotfix1_prod.version_name, tag_hotfix1_prod)

        # Hotfix 2
        self.assertEqual(expected_output_hotfix2_release, actual_output_hotfix2_release)
        self.assertEqual(expected_output_hotfix2_release.version_name, tag_hotfix2_release)

        self.assertEqual(expected_output_hotfix2_beta, actual_output_hotfix2_beta)
        self.assertEqual(expected_output_hotfix2_beta.version_name, tag_hotfix2_beta)

        self.assertEqual(expected_output_hotfix2_prod, actual_output_hotfix2_prod)
        self.assertEqual(expected_output_hotfix2_prod.version_name, tag_hotfix2_prod)

    def test_breaking_then_hotfixes(self) -> None:
        """Test Case: Run the action after a ``feat!:`` commit and after two hotfixes."""
        # Arrange
        # Breaking
        args_breaking_release = ActionInputs(
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='',
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
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='',
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
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='',
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
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_breaking_release = run_action(args_breaking_release)
        tag_breaking_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_breaking_beta = run_action(args_breaking_beta)
        tag_breaking_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_breaking_prod = run_action(args_breaking_prod)
        tag_breaking_prod = self.repo.get_latest_tag_name()

        # Hotfix 1
        self.repo.checkout('main')
        commit = self.repo.commit(CommitMessages.FIX)

        self.repo.cherrypick(commit, 'release')
        actual_output_hotfix1_release = run_action(args_hotfix1_release)
        tag_hotfix1_release = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-beta')
        actual_output_hotfix1_beta = run_action(args_hotfix1_beta)
        tag_hotfix1_beta = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-prod')
        actual_output_hotfix1_prod = run_action(args_hotfix1_prod)
        tag_hotfix1_prod = self.repo.get_latest_tag_name()

        # Hotfix 2
        self.repo.checkout('main')
        commit = self.repo.commit(CommitMessages.FIX)

        self.repo.cherrypick(commit, 'release')
        actual_output_hotfix2_release = run_action(args_hotfix2_release)
        tag_hotfix2_release = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-beta')
        actual_output_hotfix2_beta = run_action(args_hotfix2_beta)
        tag_hotfix2_beta = self.repo.get_latest_tag_name()

        self.repo.cherrypick(commit, 'release-prod')
        actual_output_hotfix2_prod = run_action(args_hotfix2_prod)
        tag_hotfix2_prod = self.repo.get_latest_tag_name()

        # Assert
        # Breaking
        self.assertEqual(expected_output_breaking_release, actual_output_breaking_release)
        self.assertEqual(expected_output_breaking_release.version_name, tag_breaking_release)

        self.assertEqual(expected_output_breaking_beta, actual_output_breaking_beta)
        self.assertEqual(expected_output_breaking_beta.version_name, tag_breaking_beta)

        self.assertEqual(expected_output_breaking_prod, actual_output_breaking_prod)
        self.assertEqual(expected_output_breaking_prod.version_name, tag_breaking_prod)

        # Hotfix 1
        self.assertEqual(expected_output_hotfix1_release, actual_output_hotfix1_release)
        self.assertEqual(expected_output_hotfix1_release.version_name, tag_hotfix1_release)

        self.assertEqual(expected_output_hotfix1_beta, actual_output_hotfix1_beta)
        self.assertEqual(expected_output_hotfix1_beta.version_name, tag_hotfix1_beta)

        self.assertEqual(expected_output_hotfix1_prod, actual_output_hotfix1_prod)
        self.assertEqual(expected_output_hotfix1_prod.version_name, tag_hotfix1_prod)

        # Hotfix 2
        self.assertEqual(expected_output_hotfix2_release, actual_output_hotfix2_release)
        self.assertEqual(expected_output_hotfix2_release.version_name, tag_hotfix2_release)

        self.assertEqual(expected_output_hotfix2_beta, actual_output_hotfix2_beta)
        self.assertEqual(expected_output_hotfix2_beta.version_name, tag_hotfix2_beta)

        self.assertEqual(expected_output_hotfix2_prod, actual_output_hotfix2_prod)
        self.assertEqual(expected_output_hotfix2_prod.version_name, tag_hotfix2_prod)


if __name__ == '__main__':
    unittest.main()
