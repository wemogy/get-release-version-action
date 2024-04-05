import logging
import logging.config
import unittest
from pathlib import Path

import yaml

from utils import *


def setup_logging() -> None:
    """Setup logging"""
    config_file = Path(__file__).resolve().parent / 'logging.config.yaml'

    with config_file.open('r') as config_stream:
        config = yaml.load(config_stream, yaml.SafeLoader)

    logging.config.dictConfig(config)
    logging.getLogger().setLevel(logging.DEBUG)


class ActionTestCase(unittest.TestCase):
    repo: TestRepo

    @classmethod
    def setUpClass(cls):
        setup_logging()

    def setUp(self):
        self.repo = TestRepo()

    def tearDown(self):
        self.repo.close()

    def test_initial(self):
        # Arrange
        args_release = ActionArguments(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_release = ActionOutputs(
            version='0.0.0-pre',
            version_name='v0.0.0-pre',
            previous_version='',
            previous_version_name='',
            has_changes=False
        )

        args_beta = ActionArguments(
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_beta = ActionOutputs(
            version='0.0.0-beta',
            version_name='v0.0.0-beta',
            previous_version='',
            previous_version_name='',
            has_changes=False
        )

        args_prod = ActionArguments(
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
            create_tag=True
        )

        expected_output_prod = ActionOutputs(
            version='0.0.0',
            version_name='v0.0.0',
            previous_version='',
            previous_version_name='',
            has_changes=False
        )

        # Act
        self.repo.checkout('release')
        actual_output_release = run_action(args_release)

        self.repo.checkout('release-beta')
        actual_output_beta = run_action(args_beta)

        self.repo.checkout('release-prod')
        actual_output_prod = run_action(args_prod)

        # Assert
        self.assertEqual(expected_output_release, actual_output_release)
        self.assertEqual(expected_output_beta, actual_output_beta)
        self.assertEqual(expected_output_prod, actual_output_prod)

    def test_first_fix(self):
        # Arrange
        args_release = ActionArguments(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_release = ActionOutputs(
            version='0.0.1-pre',
            version_name='v0.0.1-pre',
            previous_version='',
            previous_version_name='',
            has_changes=True
        )

        args_beta = ActionArguments(
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_beta = ActionOutputs(
            version='0.0.1-beta',
            version_name='v0.0.1-beta',
            previous_version='',
            previous_version_name='',
            has_changes=False
        )

        args_prod = ActionArguments(
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
            create_tag=True
        )

        expected_output_prod = ActionOutputs(
            version='0.0.1',
            version_name='v0.0.1',
            previous_version='',
            previous_version_name='',
            has_changes=False
        )

        # Act
        self.repo.commit(CommitMessages.FIX)

        self.repo.merge('main', 'release')
        actual_output_release = run_action(args_release)

        self.repo.merge('release', 'release-beta')
        actual_output_beta = run_action(args_beta)

        self.repo.merge('release-beta', 'release-prod')
        actual_output_prod = run_action(args_prod)

        # Assert
        self.assertEqual(expected_output_release, actual_output_release)
        self.assertEqual(expected_output_beta, actual_output_beta)
        self.assertEqual(expected_output_prod, actual_output_prod)

    def test_first_feature(self):
        # Arrange
        args_release = ActionArguments(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_release = ActionOutputs(
            version='0.1.0-pre',
            version_name='v0.1.0-pre',
            previous_version='',
            previous_version_name='',
            has_changes=True
        )

        args_beta = ActionArguments(
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_beta = ActionOutputs(
            version='0.1.0-beta',
            version_name='v0.1.0-beta',
            previous_version='',
            previous_version_name='',
            has_changes=False
        )

        args_prod = ActionArguments(
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
            create_tag=True
        )

        expected_output_prod = ActionOutputs(
            version='0.1.0',
            version_name='v0.1.0',
            previous_version='',
            previous_version_name='',
            has_changes=False
        )

        # Act
        self.repo.commit(CommitMessages.FEATURE)

        self.repo.merge('main', 'release')
        actual_output_release = run_action(args_release)

        self.repo.merge('release', 'release-beta')
        actual_output_beta = run_action(args_beta)

        self.repo.merge('release-beta', 'release-prod')
        actual_output_prod = run_action(args_prod)

        # Assert
        self.assertEqual(expected_output_release, actual_output_release)
        self.assertEqual(expected_output_beta, actual_output_beta)
        self.assertEqual(expected_output_prod, actual_output_prod)

    def test_first_breaking(self):
        # Arrange
        args_release = ActionArguments(
            prefix='v',
            suffix='pre',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_release = ActionOutputs(
            version='1.0.0-pre',
            version_name='v1.0.0-pre',
            previous_version='',
            previous_version_name='',
            has_changes=True
        )

        args_beta = ActionArguments(
            prefix='v',
            suffix='beta',
            previous_version_suffix='pre',
            create_tag=True
        )

        expected_output_beta = ActionOutputs(
            version='1.0.0-beta',
            version_name='v1.0.0-beta',
            previous_version='',
            previous_version_name='',
            has_changes=False
        )

        args_prod = ActionArguments(
            prefix='v',
            suffix='',
            previous_version_suffix='beta',
            create_tag=True
        )

        expected_output_prod = ActionOutputs(
            version='1.0.0',
            version_name='v1.0.0',
            previous_version='',
            previous_version_name='',
            has_changes=False
        )

        # Act
        self.repo.commit(CommitMessages.BREAKING_FEATURE)

        self.repo.merge('main', 'release')
        actual_output_release = run_action(args_release)

        self.repo.merge('release', 'release-beta')
        actual_output_beta = run_action(args_beta)

        self.repo.merge('release-beta', 'release-prod')
        actual_output_prod = run_action(args_prod)

        # Assert
        self.assertEqual(expected_output_release, actual_output_release)
        self.assertEqual(expected_output_beta, actual_output_beta)
        self.assertEqual(expected_output_prod, actual_output_prod)


if __name__ == '__main__':
    unittest.main()
