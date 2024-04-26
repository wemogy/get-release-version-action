"""The main algorithm."""
import logging
import os

import git

from ..models import Inputs, Outputs
from ..utils import create_git_tag
from .hash_based import get_next_version as get_next_version_hash
from .semantic import get_next_version as get_next_semantic_version

__all__ = [
    'main_algorithm'
]

logger = logging.getLogger('wemogy.get-release-version-action')


def main_algorithm(inputs: Inputs) -> Outputs:
    """The main algorithm."""
    logger.debug('Inputs: %s', inputs)

    # If create_tag is true, a git email address and a username are required.
    if inputs.create_tag:
        if inputs.git_email is None or inputs.git_username is None:
            raise ValueError('git email and username are required when a tag should be created!')

    with git.Repo(os.getcwd()) as repo:
        if inputs.mode == 'semantic':
            previous_version_tag_name, new_version, version_bumped = get_next_semantic_version(inputs, repo)
        elif inputs.mode == 'hash-based':
            previous_version_tag_name, new_version, version_bumped = get_next_version_hash(inputs, repo)
        else:
            raise ValueError(f'Expected input "mode" to be either "semantic" or "hash-based", but got "{inputs.mode}".')

        if inputs.suffix is not None:
            if '-' in new_version:
                # The suffix should go before the bumping suffix, that's why the dash is replaced.
                new_version = new_version.replace('-', f'-{inputs.suffix}-', 1)
            else:
                new_version += f'-{inputs.suffix}'

        new_version_tag_name = f'{inputs.prefix}{new_version}'

        new_tag_needed = (version_bumped or
                          ('0.0.0' not in new_version_tag_name and previous_version_tag_name != new_version_tag_name))

        if inputs.create_tag and new_tag_needed:
            create_git_tag(new_version_tag_name, inputs.git_username, inputs.git_email)

        output = Outputs(
            version=new_version,
            version_name=new_version_tag_name,
            previous_version=(previous_version_tag_name or '').removeprefix(inputs.prefix),
            previous_version_name=previous_version_tag_name or '',
            tag_created=new_tag_needed
        )

        logger.info('Outputs: %s', output)
        return output
