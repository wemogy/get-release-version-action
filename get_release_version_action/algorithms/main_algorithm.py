"""The main algorithm."""
import logging
import os

import git
from semver import Version

from ..models import Inputs, Outputs
from ..utils import create_git_tag
from .hash_based import get_next_version as get_next_version_hash
from .semantic import get_next_version as get_next_semantic_version

__all__ = [
    'main_algorithm'
]

logger = logging.getLogger('wemogy.get-release-version-action')


def _apply_suffix(version: str, suffix: str | None) -> str:
    """Insert ``suffix`` before the prerelease (if any), matching the action's legacy tag naming."""
    if suffix is None:
        return version
    if '-' in version:
        # The suffix goes before the bumping suffix, so replace the first dash.
        return version.replace('-', f'-{suffix}-', 1)
    return f'{version}-{suffix}'


def main_algorithm(inputs: Inputs) -> Outputs:
    """The main algorithm."""
    logger.debug('Inputs: %s', inputs)

    # If create_tag is true, a git email address and a username are required.
    if inputs.create_tag:
        if inputs.git_email is None or inputs.git_username is None:
            raise ValueError('git email and username are required when a tag should be created!')

    with git.Repo(os.getcwd()) as repo:
        if inputs.mode == 'semantic':
            previous_version_tag_name, bare_version, version_bumped = get_next_semantic_version(inputs, repo)
        elif inputs.mode == 'hash-based':
            previous_version_tag_name, bare_version, version_bumped = get_next_version_hash(inputs, repo)
        else:
            raise ValueError(f'Expected input "mode" to be either "semantic" or "hash-based", but got "{inputs.mode}".')

        new_version = _apply_suffix(bare_version, inputs.suffix)
        new_version_tag_name = f'{inputs.prefix}{new_version}'

        new_tag_needed = (version_bumped or
                          ('0.0.0' not in new_version_tag_name and previous_version_tag_name != new_version_tag_name))

        # Collision avoidance for suffix bumps: if the computed tag name already exists (e.g. left over from a
        # reverted deploy), keep bumping the prerelease counter until the name is free. This is only safe for
        # ``only_bump_suffix`` mode, where "bump further" just means incrementing the hotfix counter.
        if (inputs.only_bump_suffix and inputs.mode == 'semantic' and new_tag_needed):
            existing_tag_names = {tag.name for tag in repo.tags}
            while new_version_tag_name in existing_tag_names:
                logger.warning(
                    'Tag %s already exists; bumping %s to avoid a collision',
                    new_version_tag_name, inputs.bumping_suffix
                )
                bare_version = str(Version.parse(bare_version).bump_prerelease(inputs.bumping_suffix))
                new_version = _apply_suffix(bare_version, inputs.suffix)
                new_version_tag_name = f'{inputs.prefix}{new_version}'

        if inputs.create_tag and new_tag_needed:
            if inputs.git_email is None or inputs.git_username is None:
                raise ValueError('git email and username are required when a tag should be created!')

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
