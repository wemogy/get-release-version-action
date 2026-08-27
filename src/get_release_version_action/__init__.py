"""GitHub Action to determine the next version using Conventional Commits with support for hotfix changes."""

__all__ = [
    'Inputs',
    'Outputs',
    'cli_entrypoint',
    'main_algorithm',
]

from .algorithms import cli_entrypoint, main_algorithm
from .models import Inputs, Outputs
