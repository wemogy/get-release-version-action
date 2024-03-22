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
| ---------------------- | -------- | -------- | ----------------------------------------------------------------------- |
| `prefix`               | `false`  | `v`      | The prefix that should be prepended to the version.                     |
| `suffix`               | `false`  | `hotfix` | The suffix that should be incremented / appended to the version.        |
| `only-increase-suffix` | `false`  | `false`  | Increment the suffix if any changes got detected.                       |
| `create-tag`           | `false`  | `true`   | Create a Git Tag for the version and push it if a remote is configured. |

## Outputs

| Output                  | Description                               |
|-------------------------|-------------------------------------------|
| `version`               | The next version, without the prefix.     |
| `version-name`          | The next version, with the prefix.        |
| `previous-version`      | The previous version, without the prefix. |
| `previous-version-name` | The previous version, with the prefix.    |
| `has-changes`           | If any relevant changes got detected.     |

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

1. Run the test script with `bash test.sh`.
2. The test files are available in the folder `test`. There is also a debug log there.
3. To exit the test and delete all files, press any key in the terminal.

## FAQ

### The version stopped incrementing and keeps the same - what's wrong?

If the version number is not incrementing, please check the following points:

- The commit messages **must** follow the [Conventional Commits](https://www.conventionalcommits.org/) specification
- Cleanup the tags in the repository - that means that you need to go to the `All tags` overview and delete all tags
  which have **not** the `Verified` badge

## Why did we implemented the sematic release by ourself?

We had this issue, which finally led to the decision to implement the semantic release by ourself:

### Release branch of stage (e.g. release-beta) is always creating hotfix versions

#### How to reproduce

1. Ensure that all branches (main, release, release-beta) are in sync

2. Create a new commit `fix: hotfix` in the main branch

3. Push the commit to the main branch

4. Cherry-pick the commit to the release-beta branch

5. After a bit waiting, merge from main into release => correct version gets created

6. Merge from release into release-beta => hotfix version gets created (this could be because the cherry-pick duplicated the commit: <https://www.atlassian.com/git/tutorials/cherry-pick#:~:text=git%20cherry%2Dpick%20is%20a,be%20useful%20for%20undoing%20changes.>)

- I can confirm by checking the history that there is a duplicated commit in the release-beta branch

- For me the merge commit which is tagged to the newest version is the newest commit in the release-beta branch => don't understand why the duplicated commit is an issue

#### What causes the issue?

1. `Semantic-Release` is checking the commit history for the latest full release version

   - Prints `algorithm.next_version: The last full ...` (e.g. `algorithm.next_version: The last full release was 0.1.2, tagged as 'v0.1.2'`)

2. `Semantic-Release` is fetching all commits which are reachable from the current branch, but not from the latest full release version

   - Using `git rev-list v0.1.2... --` to get the commits

3. The unreachable commits are basically in this case two types:

   1. The merge commits in the release-beta branch

   2. The cherry-picked commit in the release-beta branch

==> The issue is that the unreachable commits are from all time, not only from the last full release version
