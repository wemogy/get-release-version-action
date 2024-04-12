"""
A GitHub Action to determine the next version by checking the commit history
for Conventional Commits with support for hotfix changes.
"""
from .models import Inputs, Outputs
from .algorithms import main

__all__ = [
    'Inputs',
    'Outputs',
    'main'
]
