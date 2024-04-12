"""Outputs of the get-release-version-action."""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass

__all__ = [
    'Outputs',
    'GetNextVersionOutput'
]

GetNextVersionOutput = tuple[str | None, str, bool]


@dataclass(frozen=True, kw_only=True)
class Outputs:
    """Outputs of the get-release-version-action."""
    version: str
    """The next version, without the prefix."""

    version_name: str
    """The next version, with the prefix."""

    previous_version: str
    """The previous version, without the prefix."""

    previous_version_name: str
    """The previous version, with the prefix."""

    tag_created: bool
    """If any relevant changes got detected."""

    def to_github_output(self) -> str:
        """Convert the outputs into the GitHub actions output format."""
        output = ''

        for name, value in dataclasses.asdict(self).items():
            output += f'{name.replace('_', '-')}='

            if isinstance(value, bool):
                output += f'{str(value).lower()}\n'
            else:
                output += f'{value}\n'

        return output
