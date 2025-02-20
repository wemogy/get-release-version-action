"""Algorithms for the get-release-version-action."""

from .cli import cli_entrypoint
from .main_algorithm import main_algorithm

__all__ = ['cli_entrypoint', 'main_algorithm']
