# Contributing

You should be using an IDE, otherwise start there...

Formatting (this is done by you):

- Black (.py)
- Prettier (.yml;.yaml;.json;.md)

Linting (this is checked by actions):

- Flake8 (.py)
- ShellCheck (.sh)

## Running Locally

To run actions locally you can use act: https://github.com/nektos/act

1. Install `act`: https://nektosact.com/installation/index.html
2. Create a `.secrets` file with: `GITHUB_TOKEN="ghp_xxx"`
3. Run `act -j test`

Note: You need to have your current commit pushed as this makes a tag on GitHub to the current sha.
This means the `test` will most likely fail on a third-party PR since the automatic GITHUB_TOKEN won't have write access to content.

To see all available jobs run: `act -l`
