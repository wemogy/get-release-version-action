"""Get the next version based on conventional commits and semantic versioning."""
import logging
import git
from semantic_release import LevelBump, ParseError
from semantic_release.commit_parser import AngularCommitParser, AngularParserOptions
from semver import Version

from ..models import Inputs, GetNextVersionOutput
from ..utils import get_sorted_tags

logger = logging.getLogger('wemogy.get-release-version-action.semantic')

__all__ = [
    'get_next_version'
]


def get_current_version(
        repo: git.Repo,
        prefix: str,
        suffix: str | None,
        bumping_suffix: str,
        reference_version_suffix: str | None
) -> git.TagReference | None:
    """
    GGet the current version (= the latest git tag that matches the versioning schema).
    If there are no tags, return ``None``.
    """
    for tag in get_sorted_tags(repo):
        if not tag.name.startswith(prefix):
            continue

        if reference_version_suffix is None:
            if suffix is None:
                dash_count = tag.name.count('-')

                if bumping_suffix in tag.name and dash_count == 1:
                    logger.debug(
                        'Found tag %s (%s) with prefix "%s" and suffix "%s"',
                        tag.name, tag.commit.hexsha, prefix, suffix
                    )
                    return tag

                if dash_count == 0:
                    logger.debug(
                        'Found tag %s (%s) with prefix "%s" and suffix "%s"',
                        tag.name, tag.commit.hexsha, prefix, suffix
                    )
                    return tag
                continue

            if suffix in tag.name:
                logger.debug(
                    'Found tag %s (%s) with prefix "%s" and suffix "%s"',
                    tag.name, tag.commit.hexsha, prefix, suffix
                )
                return tag

            continue

        # Check if the not bumped version has the reference version suffix
        if tag.name.endswith(reference_version_suffix):
            logger.debug(
                'Found tag %s (%s) with prefix "%s" and suffix "%s"',
                tag.name, tag.commit.hexsha, prefix, reference_version_suffix
            )
            return tag

        # Check if the bumped version has the current suffix
        if suffix is None:
            dash_count = tag.name.count('-')
            if dash_count != 1:
                continue

            if f'-{bumping_suffix}' in tag.name:
                logger.debug(
                    'Found tag %s (%s) with prefix "%s" and suffix "%s"',
                    tag.name, tag.commit.hexsha, prefix, suffix
                )
                return tag
            
            continue

        if f'{suffix}-{bumping_suffix}' in tag.name:
            logger.debug(
                'Found tag %s (%s) with prefix "%s" and suffix "%s"',
                tag.name, tag.commit.hexsha, prefix, suffix
            )
            return tag

    logger.debug(
        'Found no tags that have the prefix "%s" and suffix "%s" / "%s"',
        prefix, suffix, reference_version_suffix
    )
    return None


def get_new_commits(repo: git.Repo, tag: git.TagReference | None) -> list[git.Commit]:
    """Get all commits newer than the specified tag."""
    max_commits = 50
    commit_offset = 0
    reached_starting_tag = False
    new_commits: list[git.Commit] = []

    while not reached_starting_tag:
        try:
            commits = repo.iter_commits(max_count=max_commits, skip=commit_offset)
        except ValueError:
            logger.warning('No commits found')
            return []

        i = 0

        for commit in commits:
            i += 1

            if tag is None:
                logger.debug('Commit %s was found', commit.hexsha)
                new_commits.append(commit)
                continue

            if commit == tag.commit:
                logger.debug(
                    'Commit %s is current version %s (%s)',
                    commit.hexsha, tag.name, tag.commit.hexsha
                )
                reached_starting_tag = True
                break

            logger.debug(
                'Commit %s is newer than current version %s (%s)',
                commit.hexsha, tag.name, tag.commit.hexsha
            )
            new_commits.append(commit)

        commit_offset += max_commits

        if i < max_commits:
            logger.debug('Reached the end of the commit history')
            break

    return new_commits


def analyze_commits(
        repo: git.Repo,
        current_version_tag: git.TagReference | None,
        current_version: str | None
) -> tuple[str, bool]:
    """Determine the next version."""
    # 1. Add all commits to a list until the commit with the current_version_tag is reached
    new_commits = get_new_commits(repo, current_version_tag)

    # 2. Apply conventional commits to the list
    commit_parser = AngularCommitParser(AngularParserOptions())
    parsing_results = [commit_parser.parse(commit) for commit in new_commits]

    # 3. Check if the list contains major, minor or patch
    # Reduce the parsing results to an integer: 0 = chore / unknown, 1 = patch, 2 = minor, 3 = major
    commit_bumps = [
        0 if isinstance(result, ParseError) else
        3 if result.bump == LevelBump.MAJOR else
        2 if result.bump == LevelBump.MINOR else
        1 if result.bump == LevelBump.PATCH else
        0
        for result in parsing_results
    ]

    # The maximum of the numbers in commit_bumps is the version needed to be bumped
    version_to_bump = max(commit_bumps, default=0)
    logger.debug(
        'Version to bump is %s (0 = chore / unknown, 1 = patch, 2 = minor, 3 = major)',
        version_to_bump
    )

    # 4. Bump the version
    current_version_obj = Version.parse(current_version or '0.0.0')

    if version_to_bump == 1:
        return str(current_version_obj.bump_patch()), True
    if version_to_bump == 2:
        return str(current_version_obj.bump_minor()), True
    if version_to_bump == 3:
        return str(current_version_obj.bump_major()), True

    return current_version or '0.0.0', False


def get_next_version(inputs: Inputs, repo: git.Repo) -> GetNextVersionOutput:
    """
    Get the next version based on conventional commits and semantic versioning.

    :returns: A tuple of the current version name, the next version and if the version was bumped.
    """
    # The reference version is the latest version, possibly on another branch / channel.
    # It is used to get the next version.
    reference_version_tag = get_current_version(
        repo,
        inputs.prefix,
        inputs.suffix,
        inputs.bumping_suffix,
        inputs.reference_version_suffix
    )

    # The current version is the latest version on this branch / channel.
    # It is the version in the previous-version action output.
    current_version_tag = get_current_version(
        repo,
        inputs.prefix,
        inputs.suffix,
        inputs.bumping_suffix,
        None
    )

    current_version_tag_name = current_version_tag.name if current_version_tag is not None else None

    # Remove the prefix and suffix from the reference version
    if reference_version_tag is None:
        reference_version: str | None = None
    else:
        reference_version = reference_version_tag.name.removeprefix(inputs.prefix)

        if inputs.reference_version_suffix is not None:
            reference_version = reference_version.replace(f'-{inputs.reference_version_suffix}', '', 1)

        if inputs.suffix is not None:
            reference_version = reference_version.replace(f'-{inputs.suffix}', '', 1)

    next_version, version_bumped = analyze_commits(repo, reference_version_tag, reference_version)

    # No change that requires a semantic version increase
    if not version_bumped:
        logger.info('No changes detected, version stays the same.')
        return (
            current_version_tag_name,
            next_version,
            version_bumped
        )

    # Hotfix
    if inputs.only_bump_suffix:
        logger.info('Only the suffix will be incremented.')
        return (
            current_version_tag_name,
            str(Version.parse(reference_version or '0.0.0').bump_prerelease(inputs.bumping_suffix)),
            version_bumped
        )

    # Example case: New Release
    logger.info('Semantic Version will be incremented.')
    return (
        current_version_tag_name,
        next_version,
        version_bumped
    )
