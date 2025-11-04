import json
import os

from github import Auth, Github, GithubException
from yaml import Loader, load


version: str = os.environ.get("GITHUB_WORKFLOW_REF", "") or "Source Build"
print(f"GITHUB_WORKFLOW_REF: {version}")
version = version.rsplit("/", 1)[-1]
print(f"version: {version}")

print(f"🏳️ Starting Python Test Action - {version}")


# Inputs

input_tag = os.environ.get("INPUT_TAG").strip()
print(f"input_tag: {input_tag}")
input_summary: str = os.environ.get("INPUT_SUMMARY", "").strip().lower()
print(f"input_summary: {input_summary}")
input_token: str = os.environ.get("INPUT_TOKEN", "").strip()
print(f"input_token: {input_token}")

# Parse JSON or YAML Input Data
input_data = os.environ.get("INPUT_DATA", "").strip()
print(f"input_data: \033[36;1m{input_data}")
try:
    data = json.loads(input_data)
except Exception as error:
    print(f"::debug::{error}")
    try:
        data = load(input_data, Loader=Loader)
    except Exception as error:
        print(f"::debug::{error}")
        data = None
print(f"data: \033[36;1m{data}")


owner: str = os.environ.get("GITHUB_REPOSITORY", "").split("/")[0]
repo: str = os.environ.get("GITHUB_REPOSITORY", "").split("/")[1]
print(f"owner: {owner}")
print(f"repo: {repo}")

sha: str = os.environ.get("GITHUB_SHA", "")
print(f"sha: {sha}")


# Action

g = Github(auth=Auth.Token(input_token))
r = g.get_repo(f"{owner}/{repo}")
print(f"repo.name: {r.name}")
print(f"repo.full_name: {r.full_name}")

try:
    ref = r.get_git_ref(f"tags/{input_tag}")
    if ref.object.sha != sha:
        print(f"Updating: {input_tag} -> {ref.object.sha}")
        ref.edit(sha, True)
        result = "Updated"
    else:
        print(f"Unchanged: {input_tag} -> {ref.object.sha}")
        result = "Unchanged"

except GithubException:
    ref = r.create_git_ref(f"refs/tags/{input_tag}", sha)
    print(f"Created: {ref.ref} -> {ref.object.sha}")
    result = "Created"

g.close()

print(f"ref.ref: {ref.ref}")
print(f"ref.object.sha: {ref.object.sha}")


# Outputs
# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    print(f"sha={sha}", file=f)  # type: ignore


# Summary
# https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#adding-a-job-summary

if input_summary in ["y", "yes", "true", "on"]:
    inputs_table = ["<table><tr><th>Input</th><th>Value</th></tr>"]
    for x in ["tag", "summary"]:
        value = globals()[f"input_{x}"]
        inputs_table.append(f"<tr><td>{x}</td><td>{value or '-'}</td></tr>")
    inputs_table.append("</table>")

    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
        print("### Python Test Action", file=f)  # type: ignore
        print(f"{result}: [{ref.ref}]({r.html_url}/releases/tag/{input_tag}) ➡️ `{sha}`", file=f)  # type: ignore
        print(f"<details><summary>Inputs</summary>{''.join(inputs_table)}</details>\n", file=f)  # type: ignore
        print(f"[Report an issue or request a feature]({r.html_url}/issues)", file=f)  # type: ignore


print("✅ \u001b[32;1mFinished Success")
