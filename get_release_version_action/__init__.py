"""
A GitHub Action to determine the next version by checking the commit history
for Conventional Commits with support for hotfix changes.
"""
from .algorithms import cli_entrypoint, main_algorithm
from .models import Inputs, Outputs

__all__ = [
    'Inputs',
    'Outputs',
    'main_algorithm',
    'cli_entrypoint'
]
