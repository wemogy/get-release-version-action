# ![wemogy logo](https://wemogyimages.blob.core.windows.net/logos/wemogy-github-tiny.png) Get Release Version (GitHub Action)

A GitHub Action to determine the next version by checking the commit history
for [Conventional Commits](https://www.conventionalcommits.org/) with support for hotfix changes.

## Contents

<!-- TOC -->
* [![wemogy logo](https://wemogyimages.blob.core.windows.net/logos/wemogy-github-tiny.png) Get Release Version (GitHub Action)](#-get-release-version-github-action)
  * [Contents](#contents)
  * [Usage](#usage)
    * [Inputs](#inputs)
    * [Outputs](#outputs)
  * [FAQ](#faq)
    * [The version stopped incrementing and keeps the same — what's wrong?](#the-version-stopped-incrementing-and-keeps-the-same--whats-wrong)
    * [Why did we implement sematic release by ourselves?](#why-did-we-implement-sematic-release-by-ourselves)
  * [Development](#development)
<!-- TOC -->

## Usage

```yaml
- name: Clone repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0

- uses: wemogy/get-release-version-action@v3.1.0
  id: get-release-version
  with:
    prefix: "v"
    suffix: "beta"
    previous-version-suffix: "dev"
    bumping-suffix: "hotfix"
    only-bump-suffix: "true"
    create-tag: "true"

- run: echo ${{ steps.get-release-version.outputs.version }}
- run: echo ${{ steps.get-release-version.outputs.version-name }}
- run: echo ${{ steps.get-release-version.outputs.previous-version }}
- run: echo ${{ steps.get-release-version.outputs.previous-version-name }}
- run: echo ${{ steps.get-release-version.outputs.has-changes }}
```

### Inputs

| Input                     | Required | Default    | Description                                                                                              |
|---------------------------|----------|------------|----------------------------------------------------------------------------------------------------------|
| `prefix`                  | `false`  | `v`        | The prefix that should be prepended to the version.                                                      |
| `suffix`                  | `false`  | ``         | The suffix that should be appended to the version (e.g. `beta`).                                         |
| `previous-version-suffix` | `false`  | ``         | The suffix that should be replaced with the value in `suffix` (e.g. `dev`).                              |
| `bumping-suffix`          | `false`  | `hotfix`   | The suffix to append to the version (or increment if it already exists) if `only-bump-suffix` is `true`. |
| `only-bump-suffix`        | `false`  | `false`    | Bump the `bumping-suffix` instead of the version if changes were detected.                               |
| `create-tag`              | `false`  | `true`     | Create a git tag for the version and push it if a remote is configured.                                  |
| `mode`                    | `false`  | `semantic` | The mode to use for determining the next version. Possible values: `semantic`, `hash-based`.             |

### Outputs

| Output                  | Description                               |
|-------------------------|-------------------------------------------|
| `version`               | The next version, without the prefix.     |
| `version-name`          | The next version, with the prefix.        |
| `previous-version`      | The previous version, without the prefix. |
| `previous-version-name` | The previous version, with the prefix.    |
| `has-changes`           | If any relevant changes got detected.     |

## FAQ

### The version stopped incrementing and keeps the same — what's wrong?

If the version number is not incrementing, please check the following points:

- The commit messages **must** follow the [Conventional Commits](https://www.conventionalcommits.org/) specification
- Clean up the tags in the repository - this means that you need to go to the `All tags` overview and delete all tags
  that do **not** have the `Verified` badge

### Why did we implement sematic release by ourselves?

We had this issue, which finally led to the decision to implement the semantic release by ourselves:

#### Release branch of stage (e.g. release-beta) is always creating hotfix versions

##### How to reproduce

1. Ensure that all branches (main, release, release-beta) are in sync

2. Create a new commit `fix: hotfix` in the main branch

3. Push the commit to the main branch

4. Cherry-pick the commit to the release-beta branch

5. After a bit waiting, merge from main into release => correct version gets created

6. Merge from release into release-beta => hotfix version gets created (this could be because the cherry-pick duplicated the commit: <https://www.atlassian.com/git/tutorials/cherry-pick#:~:text=git%20cherry%2Dpick%20is%20a,be%20useful%20for%20undoing%20changes.>)

- I can confirm by checking the history that there is a duplicated commit in the release-beta branch

- For me the merge commit which is tagged to the newest version is the newest commit in the release-beta branch => don't understand why the duplicated commit is an issue

##### What causes the issue?

1. `Semantic-Release` is checking the commit history for the latest full release version

   - Prints `algorithm.next_version: The last full ...` (e.g. `algorithm.next_version: The last full release was 0.1.2, tagged as 'v0.1.2'`)

2. `Semantic-Release` is fetching all commits which are reachable from the current branch, but not from the latest full release version

   - Using `git rev-list v0.1.2... --` to get the commits

3. The unreachable commits are basically in this case two types:

   1. The merge commits in the release-beta branch

   2. The cherry-picked commit in the release-beta branch

==> The issue is that the unreachable commits are from all time, not only from the last full release version

## Development

This project uses [poetry](https://python-poetry.org/docs/#installation) for dependency management.

### Install dependencies

```bash
# working directory: repository root
poetry install
```

### Activate the poetry shell

```bash
# working directory: repository root
poetry shell
```

### Run the script

```bash
# with poetry shell
# working directory: src
python3 app.py [...args]
```

### Run the Docker container

Build:

```bash
# working directory: repository root
docker build -t get-release-version-action:local -f Dockerfile .
```

Run:

```bash
# working directory: repository root
docker run get-release-version-action:local
```

### Run the tests

```bash
# with poetry shell
# working directory: tests
python3 -m unittest
```
