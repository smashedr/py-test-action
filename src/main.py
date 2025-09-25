import os

from github import Auth, Github, GithubException


version: str = os.environ.get("GITHUB_ACTION_PATH", "Dev Build")
print(f"GITHUB_ACTION_PATH: {version}")
version = version.rsplit("/", 1)[-1]
print(f"version: {version}")

print(f"🏳️ Starting Python Test Action - {version}")


# Inputs

input_tag = os.environ.get("INPUT_TAG")
print(f"input_tag: {input_tag}")
input_summary: str = os.environ.get("INPUT_SUMMARY", "").strip().lower()
print(f"input_summary: {input_summary}")
input_token: str = os.environ.get("INPUT_TOKEN", "")
print(f"input_token: {input_token}")

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
    print(f"sha={sha}", file=f)


# Summary
# https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#adding-a-job-summary

if input_summary in ["y", "yes", "true", "on"]:
    inputs_table = ["<table><tr><th>Input</th><th>Value</th></tr>"]
    for x in ["tag", "summary"]:
        value = globals()[f"input_{x}"]
        inputs_table.append(f"<tr><td>{x}</td><td>{value or '-'}</td></tr>")
    inputs_table.append("</table>")

    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
        print("### Python Test Action", file=f)
        print(f"{result}: [{ref.ref}]({r.html_url}/releases/tag/{input_tag}) ➡️ `{sha}`", file=f)
        print(f"<details><summary>Inputs</summary>{''.join(inputs_table)}</details>\n", file=f)
        print(f"[Report an issue or request a feature]({r.html_url}/issues)", file=f)


print("✅ \u001b[32;1mFinished Success")


# Commands
# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
# print("::notice::Notice Annotation")
# print("::warning::Warning Annotation")
# print("::error::Error Annotation")


# Colors
# print("\033[37;1m White Bold")
# print("\033[36;1m Cyan Bold")
# print("\033[35;1m Magenta Bold")
# print("\033[34;1m Blue Bold")
# print("\033[33;1m Yellow Bold")
# print("\033[32;1m Green Bold")
# print("\033[31;1m Red Bold")
# print("\033[30;1m Grey Bold")
# print("\033[37m White")
# print("\033[36m Cyan")
# print("\033[35m Magenta")
# print("\033[34m Blue")
# print("\033[33m Yellow")
# print("\033[32m Green")
# print("\033[31m Red")
# print("\033[30m Grey")
# print("\033[0m RESET")
