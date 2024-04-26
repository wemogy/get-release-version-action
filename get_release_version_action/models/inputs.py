"""Inputs of the get-release-version-action."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from inspect import get_annotations
import logging
from types import NoneType, UnionType
from typing import Any, get_args

__all__ = [
    'Inputs'
]

logger = logging.getLogger('wemogy.get-release-version-action')


@dataclass(frozen=True, kw_only=True)
class Inputs:
    """Inputs of the get-release-version-action."""

    prefix: str = 'v'
    """The prefix that should be prepended to the version."""

    suffix: str | None = None
    """The suffix that should be appended to the version (e.g. `beta`)."""

    reference_version_suffix: str | None = None
    """The suffix that should be replaced with the value in `suffix` (e.g. `dev`)."""

    bumping_suffix: str = 'hotfix'
    """The suffix to append to the version (or increment if it already exists) if `only_bump_suffix` is `true`."""

    only_bump_suffix: bool = False
    """Bump the `bumping_suffix` instead of the version if changes were detected."""

    create_tag: bool = True
    """Create a git tag for the version and push it if a remote is configured."""

    git_username: str | None = None
    """The username for creating the (annotated) git tag. Use `NONE` for no username."""

    git_email: str | None = None
    """The email address for creating the (annotated) git tag. Use `NONE` for no email address."""

    mode: str = 'semantic'
    """The mode to use for determining the next version. Possible values: `semantic`, `hash-based`."""

    @classmethod
    def from_argparse(cls, args: argparse.Namespace) -> Inputs:
        """Convert the ``argparse`` Namespace into an inputs object."""
        ctor_args: dict[str, Any] = {}
        input_properties = get_annotations(cls, eval_str=True)

        for property_name, property_type in input_properties.items():
            raw_value: Any = getattr(args, property_name)
            value: Any

            if property_type is bool:
                if raw_value.lower() == 'true':
                    value = True
                elif raw_value.lower() == 'false':
                    value = False
                else:
                    raise TypeError(
                        f'Expected boolean input "{property_name}"'
                        f' to be either "true" or "false", but got "{raw_value}".'
                        )

            elif property_type is str:
                value = raw_value

            # Docker seems to have problems with passing empty strings as arguments.
            # Because of that, a string containing 'NONE' is considered empty / as None.
            elif isinstance(property_type, UnionType) \
                    and str in get_args(property_type) \
                    and NoneType in get_args(property_type):
                if raw_value.strip() == '' or raw_value.strip() == 'NONE':
                    value = None
                else:
                    value = raw_value

            else:
                value = property_type(raw_value)

            ctor_args[property_name] = value
            logger.debug('Argument %s of type %s parsed to %s', property_name, property_type, value)

        return cls(**ctor_args)  # pylint: disable=missing-kwoa
