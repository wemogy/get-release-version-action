# ![wemogy logo](https://wemogyimages.blob.core.windows.net/logos/wemogy-github-tiny.png) Get Release Version (GitHub Action)

A GitHub Action to determine if a version on a staging branch needs to be updated after a merge. It does this, by checking the commit history for [Conventional Commits](https://www.conventionalcommits.org/). If a change got detected, the version prefix will be increased.

## Usage

```yaml
- uses: wemogy/next-version-action@2.0.2
  id: release-version
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    projects: 'Single'

- run: echo ${{ steps.release-version.outputs.next-version }}
```

## Inputs

| Input | Description |
|-|-|
| `token` | **Required** A GitHub Access Token |
| `repo` | The repository name (Default: current repository) |
| `username` | The GitHub username (Default: current repository owner) |
| `branch` | The release branch to check (Default: current branch) |
| `projects` | The amount of projects in this repo (Single or Multi) (Default: Single) |
| `prefix` | A prefix to all versions and release branches (Default: v) |

## Outputs

| Output | Description |
|-|-|
| `next-version` | The next semantic version for the next release without prefix |
| `next-version-name` | The next semantic version for the next release with prefix |
| `folder` | The name of the folder for the branch |
