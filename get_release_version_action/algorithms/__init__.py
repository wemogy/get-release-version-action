"""Algorithms for the get-release-version-action."""
from .main_algorithm import main_algorithm
from .cli import cli_entrypoint

__all__ = [
   'main_algorithm',
   'cli_entrypoint'
]
