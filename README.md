# ![wemogy logo](https://wemogyimages.blob.core.windows.net/logos/wemogy-github-tiny.png) Get Release Version (GitHub Action)

A GitHub Action to determine the next version by checking the commit history for [Conventional Commits](https://www.conventionalcommits.org/).

## Usage

```yaml
- name: Clone repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0
    fetch-tags: true
    ref: ${{ github.event.pull_request.head.sha }}
- uses: wemogy/get-release-version-action@v1
  id: get-release-version
  with:
    suffix: ''
    only-increase-suffix: 'false'

- run: echo ${{ steps.get-release-version.outputs.version }}
- run: echo ${{ steps.get-release-version.outputs.has-changes }}
```

## Inputs

| Input | Description |
|-|-|
| `suffix` | The suffix to append to the version (e.g. `hotfix`) |
| `only-increase-suffix` | If set to `true`, even if changes got detected, only the suffix will be incremented |

## Outputs

| Output | Description |
|-|-|
| `version` | The version to use for the release |
| `has-changes` | Determines, if changes got detected, which require a version change according to Conventional Commits. |
