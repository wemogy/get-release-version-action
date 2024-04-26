# ![wemogy logo](https://wemogyimages.blob.core.windows.net/logos/wemogy-github-tiny.png) Get Release Version (GitHub Action)

A GitHub Action to determine the next version by checking the commit history
for [Conventional Commits](https://www.conventionalcommits.org/) with support for hotfix changes.

## Usage

```yaml
- name: Clone repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0

- uses: wemogy/get-release-version-action@v4.2.2
  id: get-release-version
  with:
    prefix: "v"
    suffix: "beta"
    reference-version-suffix: "dev"
    bumping-suffix: "hotfix"
    only-bump-suffix: "true"
    create-tag: "true"

- run: echo ${{ steps.get-release-version.outputs.version }}
- run: echo ${{ steps.get-release-version.outputs.version-name }}
- run: echo ${{ steps.get-release-version.outputs.previous-version }}
- run: echo ${{ steps.get-release-version.outputs.previous-version-name }}
- run: echo ${{ steps.get-release-version.outputs.tag-created }}
```

### Inputs

| Input                      | Required | Default    | Description                                                                                              |
|----------------------------|----------|------------|----------------------------------------------------------------------------------------------------------|
| `prefix`                   | `false`  | `v`        | The prefix that should be prepended to the version.                                                      |
| `suffix`                   | `false`  | `NONE`     | The suffix that should be appended to the version (e.g. `beta`). Use `NONE` for no suffix.               |
| `reference-version-suffix` | `false`  | `NONE`     | The suffix that should be replaced with the value in `suffix` (e.g. `dev`). Use `NONE` for no suffix.    |
| `bumping-suffix`           | `false`  | `hotfix`   | The suffix to append to the version (or increment if it already exists) if `only-bump-suffix` is `true`. |
| `only-bump-suffix`         | `false`  | `false`    | Bump the `bumping-suffix` instead of the version if changes were detected.                               |
| `create-tag`               | `false`  | `true`     | Create a git tag for the version and push it if a remote is configured.                                  |
| `mode`                     | `false`  | `semantic` | The mode to use for determining the next version. Possible values: `semantic`, `hash-based`.             |

### Outputs

| Output                  | Description                                                 |
|-------------------------|-------------------------------------------------------------|
| `version`               | The next version, without the prefix.                       |
| `version-name`          | The next version, with the prefix.                          |
| `previous-version`      | The previous version, without the prefix.                   |
| `previous-version-name` | The previous version, with the prefix.                      |
| `tag-created`           | If any relevant changes got detected and a tag got created. |

## FAQ

### The version stopped incrementing — what's wrong?

If the version number stays the same, please check the following:

- The GitHub workflow **must** use `actions/checkout@4` with `fetch-depth: 0`. This ensures that the commit and tag history is fetched, which is necessary for determining the change level and the last version.
- At least one commit message **must** follow the [Conventional Commits](https://www.conventionalcommits.org/) specification and **must not** be of the level `chore`.
- Remove all tags from the repository that do not have the `Verified` badge.

### Why did we implement sematic release by ourselves?

We had this issue, which finally led to the decision to implement the semantic release by ourselves:

> Release branch of stage (e.g. release-beta) is always creating hotfix versions.

#### How to reproduce

1. Ensure that all branches (`main`, `release`, `release-beta`) are in sync
2. Create a new commit `fix: hotfix` on the main branch
3. Push the commit to the main branch
4. Cherry-pick the commit to the `release-beta` branch
5. After a bit of waiting, merge from `main` into `release` ⇒ the correct version gets created
6. Merge from `release` into `release-beta` ⇒ a hotfix version gets created (this could be because the cherry-pick duplicated the commit: <https://www.atlassian.com/git/tutorials/cherry-pick#:~:text=git%20cherry%2Dpick%20is%20a,be%20useful%20for%20undoing%20changes.>)

- I can confirm by checking the history that there is a duplicated commit in the `release-beta` branch
- For me, the merge commit which is tagged to the newest version is the newest commit in the `release-beta` branch ⇒ I don't understand why the duplicated commit is an issue

#### What causes the issue?

1. `Semantic-Release` is checking the commit history for the latest full release version
   - Prints something like `algorithm.next_version: The last full release was 0.1.2, tagged as 'v0.1.2'`
2. `Semantic-Release` is fetching all commits that are reachable from the current branch, but not from the latest full release version
   - Using `git rev-list v0.1.2... --` to get the commits
3. The unreachable commits are basically in this case two types:
   1. The merge commits in the `release-beta` branch
   2. The cherry-picked commit in the `release-beta` branch

⇒ The issue is that the unreachable commits are from all time, not only from the last full release version.

## Development

This project uses [poetry](https://python-poetry.org/docs/#installation) for dependency management.

### Install dependencies

For development:

```bash
# working directory: repository root
poetry install --with dev
```

For production:

```bash
# working directory: repository root
poetry install --without dev
```

### Add or update dependencies

```bash
# working directory: repository root
poetry add <dependency>[@^<version>] [--group dev]
poetry update [<dependency>[@^<version>]]
```

Some dependencies are missing type definitions (stubs) for mypy.
If mypy fails with a message that a `module is installed but missing library stubs or py.typed marker`, the stubs must be created for the packages.
These stubs can be generated by mypy, but the output code is not perfect.
This means that after each run of the generator, the stubs of the code used by our code **must** be checked and adjusted.

For a newly installed package, add a new command to the code block below and run it.
Then check the functions and classes used by our code.

For an updated package, run the command for the updated package **only** if the update has changed some of the functions or classes used by our code.
Again, check those functions and classes after you run the command.

```bash
# working directory: repository root
# command template: stubgen -o .mypy_stubs -p <package_name>
stubgen -o .mypy_stubs -p semantic_release
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
pytest tests
```

The tests are isolated from the actual source code, because they are supposed to test the same interface that the action also uses.
This means that the tests **must not** import anything from the source code or vice versa.

### Run linting and type checking

This project uses pylint and flake8 for linting / code style checking and mypy for static type checking.

All tools are configured in the `pyproject.toml`.

```bash
# with poetry shell
# working directory: repository root
pylint get_release_version_action
flake8 get_release_version_action
mypy get_release_version_action

pylint tests/e2e
flake8 tests
mypy tests
```

> [!IMPORTANT]
> Source code and tests are isolated from each other and also need to be checked isolated from each other to prevent false warnings.
