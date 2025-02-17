[![Tags](https://img.shields.io/github/actions/workflow/status/smashedr/py-test-action/tags.yaml?logo=github&logoColor=white&label=tags)](https://github.com/smashedr/py-test-action/actions/workflows/tags.yaml)
[![Test](https://img.shields.io/github/actions/workflow/status/smashedr/py-test-action/test.yaml?logo=github&logoColor=white&label=test)](https://github.com/smashedr/py-test-action/actions/workflows/test.yaml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=smashedr_py-test-action&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=smashedr_py-test-action)
[![GitHub Release Version](https://img.shields.io/github/v/release/smashedr/py-test-action?logo=github)](https://github.com/smashedr/py-test-action/releases/latest)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/smashedr/py-test-action?logo=github&logoColor=white&label=updated)](https://github.com/smashedr/py-test-action/graphs/commit-activity)
[![Codeberg Last Commit](https://img.shields.io/gitea/last-commit/shaner/py-test-action/master?gitea_url=https%3A%2F%2Fcodeberg.org%2F&logo=codeberg&logoColor=white&label=updated)](https://codeberg.org/shaner/py-test-action)
[![GitHub Top Language](https://img.shields.io/github/languages/top/smashedr/py-test-action?logo=htmx&logoColor=white)](https://github.com/smashedr/py-test-action)
[![GitHub Org Stars](https://img.shields.io/github/stars/cssnr?style=flat&logo=github&logoColor=white)](https://cssnr.github.io/)
[![Discord](https://img.shields.io/discord/899171661457293343?logo=discord&logoColor=white&label=discord&color=7289da)](https://discord.gg/wXy6m2X8wY)

# Python Test Action

This action creates or updates the provided `tag` to the `sha` has that triggered the workflow.

This includes inputs, outputs, job summary, and automatic token authentication.

> [!NOTE]  
> Note: this is a simple docker action and is built every run from the Dockerfile.
> If you have a more complex build you should build and push images to GHCR.  
> For this you should instead use this template: https://github.com/smashedr/docker-test-action

- [Inputs](#Inputs)
- [Outputs](#Outputs)
- [Examples](#Examples)
- [Development](#Development)

## Inputs

| input   | required | default               | description                 |
| ------- | -------- | --------------------- | --------------------------- |
| tag     | No       | test                  | Tag to Create or Update     |
| summary | No       | true                  | Add Summary to Job          |
| token   | No       | `${{ github.token }}` | Only if External Token [^1] |

With no inputs this will create/update the tag `test`.

```yaml
- name: 'Python Test Action'
  uses: smashedr/py-test-action@v1
```

With all inputs. Note that `token` is NOT required.

```yaml
- name: 'Python Test Action'
  uses: smashedr/py-test-action@v1
  with:
    tag: test
    summary: true
    token: ${{ secrets.PAT }} # only include this if you need to use a PAT
```

### Permissions

This action requires the following permissions:

```yaml
permissions:
  contents: write
```

## Outputs

| output | description |
| ------ | ----------- |
| sha    | Tag Hash    |

```yaml
- name: 'Python Test Action'
  id: test
  uses: smashedr/py-test-action@v1

- name: 'Echo Output'
  run: |
    echo "sha: '${{ steps.test.outputs.sha }}'"
```

## Examples

```yaml
name: 'Test'

on:
  workflow_dispatch:
  push:

jobs:
  test:
    name: 'Test'
    runs-on: ubuntu-latest
    timeout-minutes: 5
    permissions:
      contents: write

    steps:
      - name: 'Checkout'
        uses: actions/checkout@v4

      - name: 'Python Test Action'
        id: test
        uses: smashedr/py-test-action@v1

      - name: 'Echo Outputs'
        run: |
          echo "sha: '${{ steps.test.outputs.sha }}'"
```

# Development

If you would like to submit a PR, please review the [CONTRIBUTING.md](CONTRIBUTING.md).

1. Install `act`: https://nektosact.com/installation/index.html
2. Create a `.secrets` file with: `GITHUB_TOKEN="ghp_xxx"`
3. Run `act -j test`

For advanced using with things like secrets, variables and context see: https://nektosact.com/usage/index.html

You should also review the options from `act --help`

Note, the `.env`, `.secrets` and `.vars` files are automatically sourced with no extra options.
To source `event.json` you need to run act with `act -e event.json`

[^1]:
    The `${{ github.token }}` / `{{ secrets.GITHUB_TOKEN }}` is automatically passed, there is no need to manually pass these!
    This is only available to allow users to pass a different token they have created and defined in their `secrets`.
