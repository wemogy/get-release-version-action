# ![wemogy logo](https://wemogyimages.blob.core.windows.net/logos/wemogy-github-tiny.png) Get Release Version (GitHub Action)

A GitHub Action to determine the next version by checking the commit history
for [Conventional Commits](https://www.conventionalcommits.org/) with support for hotfix changes.

## Usage

```yaml
- name: Clone repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0

- uses: wemogy/get-release-version-action@v2
  id: get-release-version
  with:
    prefix: "v"
    suffix: "hotfix"
    only-increase-suffix: "false"
    create-tag: "true"

- run: echo ${{ steps.get-release-version.outputs.version }}
- run: echo ${{ steps.get-release-version.outputs.version-name }}
- run: echo ${{ steps.get-release-version.outputs.has-changes }}
```

## Inputs

| Input                  | Required | Default  | Description                                                             |
|------------------------|----------|----------|-------------------------------------------------------------------------|
| `prefix`               | `false`  | `v`      | The prefix that should be prepended to the version.                     |
| `suffix`               | `false`  | `hotfix` | The suffix that should be incremented / appended to the version.        |
| `only-increase-suffix` | `false`  | `false`  | Increment the suffix if any changes got detected.                       |
| `create-tag`           | `false`  | `true`   | Create a Git Tag for the version and push it if a remote is configured. |

## Outputs

| Output         | Description                           |
|----------------|---------------------------------------|
| `version`      | The next version, without the prefix. |
| `version-name` | The next version, with the prefix.    |
| `has-changes`  | If any relevant changes got detected. |

## Docker

Build:

```bash
docker build -t get-release-version-action:local -f Dockerfile .
```

Run:

```bash
docker run get-release-version-action:local
```

## Testing

1. Create a GitHub repository with a default branch (eg. by creating a README.md).
2. Create a `.test.env` file in the repository root and set the `TEST_REPOSITORY_URL` variable to the repository created
   in step 1.
3. Run the test script with `bash test.sh`.
4. The test files are available in the folder `test`. There is also a debug log there.
5. To exit the test and delete all files, press any key in the terminal.
6. After the test, delete the GitHub repository.
   The test needs a fresh repository because it uses tags to determine the next version and creates a new tag for the
   new version,
   so if the repository already has tags, the output version is not the one expected in the test script.

## FAQ

### The version stopped incrementing and keeps the same - what's wrong?

If the version number is not incrementing, please check the following points:

- The commit messages **must** follow the [Conventional Commits](https://www.conventionalcommits.org/) specification
- Cleanup the tags in the repository - that means that you need to go to the `All tags` overview and delete all tags
  which have **not** the `Verified` badge
