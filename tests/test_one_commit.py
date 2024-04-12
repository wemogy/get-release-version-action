"""Test all scenarios where one or zero commits (beside the initial commit) are made."""
# pylint: disable=too-many-locals,too-many-lines,duplicate-code
import unittest
from unittest import TestCase

from utils import ActionInputs, ActionOutputs, CommitMessages, TestRepo, run_action, setup_logging


class OneCommitTestCase(TestCase):
    """Test all scenarios where one or zero commits (beside the initial commit) are made."""
    repo: TestRepo

    @classmethod
    def setUpClass(cls) -> None:
        setup_logging()

    def setUp(self) -> None:
        self.repo = TestRepo()

    def tearDown(self) -> None:
        self.repo.close()

    def test_initial(self) -> None:
        """Test Case: Run the action directly after the initial commit."""
        # Arrange
        args_release = ActionInputs(
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
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
            prefix='v',
            suffix='',
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
        self.repo.checkout('release')
        actual_output_release = run_action(args_release)
        tag_release = self.repo.get_latest_tag_name()

        self.repo.checkout('release-beta')
        actual_output_beta = run_action(args_beta)
        tag_beta = self.repo.get_latest_tag_name()

        self.repo.checkout('release-prod')
        actual_output_prod = run_action(args_prod)
        tag_prod = self.repo.get_latest_tag_name()

        # Assert
        self.assertEqual(expected_output_release, actual_output_release)
        self.assertEqual(None, tag_release)

        self.assertEqual(expected_output_beta, actual_output_beta)
        self.assertEqual(None, tag_beta)

        self.assertEqual(expected_output_prod, actual_output_prod)
        self.assertEqual(None, tag_prod)

    def test_chore(self) -> None:
        """Test Case: Run the action after a ``chore:`` commit."""
        # Arrange
        args_release = ActionInputs(
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
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
            prefix='v',
            suffix='',
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
        self.repo.commit(CommitMessages.CHORE)

        self.repo.merge('main', 'release')
        actual_output_release = run_action(args_release)
        tag_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_beta = run_action(args_beta)
        tag_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_prod = run_action(args_prod)
        tag_prod = self.repo.get_latest_tag_name()

        # Assert
        self.assertEqual(expected_output_release, actual_output_release)
        self.assertEqual(None, tag_release)

        self.assertEqual(expected_output_beta, actual_output_beta)
        self.assertEqual(None, tag_beta)

        self.assertEqual(expected_output_prod, actual_output_prod)
        self.assertEqual(None, tag_prod)

    def test_fix(self) -> None:
        """Test Case: Run the action after a ``fix:`` commit."""
        # Arrange
        args_release = ActionInputs(
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
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
            prefix='v',
            suffix='',
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
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_release = run_action(args_release)
        tag_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_beta = run_action(args_beta)
        tag_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_prod = run_action(args_prod)
        tag_prod = self.repo.get_latest_tag_name()

        # Assert
        self.assertEqual(expected_output_release, actual_output_release)
        self.assertEqual(expected_output_release.version_name, tag_release)

        self.assertEqual(expected_output_beta, actual_output_beta)
        self.assertEqual(expected_output_beta.version_name, tag_beta)

        self.assertEqual(expected_output_prod, actual_output_prod)
        self.assertEqual(expected_output_prod.version_name, tag_prod)

    def test_feat(self) -> None:
        """Test Case: Run the action after a ``feat:`` commit."""
        # Arrange
        args_release = ActionInputs(
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
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
            prefix='v',
            suffix='',
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
        self.repo.commit(CommitMessages.FEATURE)

        self.repo.merge('main', 'release')
        actual_output_release = run_action(args_release)
        tag_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_beta = run_action(args_beta)
        tag_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_prod = run_action(args_prod)
        tag_prod = self.repo.get_latest_tag_name()

        # Assert
        self.assertEqual(expected_output_release, actual_output_release)
        self.assertEqual(expected_output_release.version_name, tag_release)

        self.assertEqual(expected_output_beta, actual_output_beta)
        self.assertEqual(expected_output_beta.version_name, tag_beta)

        self.assertEqual(expected_output_prod, actual_output_prod)
        self.assertEqual(expected_output_prod.version_name, tag_prod)

    def test_breaking(self) -> None:
        """Test Case: Run the action after a ``feat!:`` commit."""
        # Arrange
        args_release = ActionInputs(
            prefix='v',
            suffix='pre',
            reference_version_suffix='pre',
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
            prefix='v',
            suffix='beta',
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
            prefix='v',
            suffix='',
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
        self.repo.commit(CommitMessages.BREAKING_FEATURE)

        self.repo.merge('main', 'release')
        actual_output_release = run_action(args_release)
        tag_release = self.repo.get_latest_tag_name()

        self.repo.merge('release', 'release-beta')
        actual_output_beta = run_action(args_beta)
        tag_beta = self.repo.get_latest_tag_name()

        self.repo.merge('release-beta', 'release-prod')
        actual_output_prod = run_action(args_prod)
        tag_prod = self.repo.get_latest_tag_name()

        # Assert
        self.assertEqual(expected_output_release, actual_output_release)
        self.assertEqual(expected_output_release.version_name, tag_release)

        self.assertEqual(expected_output_beta, actual_output_beta)
        self.assertEqual(expected_output_beta.version_name, tag_beta)

        self.assertEqual(expected_output_prod, actual_output_prod)
        self.assertEqual(expected_output_prod.version_name, tag_prod)


if __name__ == '__main__':
    unittest.main()
