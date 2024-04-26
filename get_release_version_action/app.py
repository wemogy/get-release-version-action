"""
A GitHub Action to determine the next version by checking the commit history
for Conventional Commits with support for hotfix changes.
"""
from get_release_version_action import cli_entrypoint

if __name__ == '__main__':
    cli_entrypoint()
