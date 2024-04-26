"""
A GitHub Action to determine the next version by checking the commit history
for Conventional Commits with support for hotfix changes.
"""
from .models import Inputs, Outputs
from .algorithms import main_algorithm, cli_entrypoint

__all__ = [
    'Inputs',
    'Outputs',
    'main_algorithm',
    'cli_entrypoint'
]