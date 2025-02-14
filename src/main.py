import os
from github import Github, Auth, GithubException

print("🏳️ Starting Python Test Action")


# Inputs

input_tag = os.environ.get("INPUT_TAG")
print(f"input_tag: {input_tag}")
input_summary = os.environ.get("INPUT_SUMMARY")
print(f"input_summary: {input_summary}")
input_token = os.environ.get("INPUT_TOKEN")
print(f"input_token: {input_token}")

owner = os.environ.get("GITHUB_REPOSITORY").split("/")[0]
repo = os.environ.get("GITHUB_REPOSITORY").split("/")[1]
print(f"owner: {owner}")
print(f"repo: {repo}")

sha = os.environ.get("GITHUB_SHA")
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

with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
    print("### Python Test Action", file=f)
    print(
        f"{result}: [{ref.ref}]({r.html_url}/releases/tag/{input_tag}) ➡️ `{sha}`",
        file=f,
    )
    print(
        f"<details><summary>Inputs</summary><table><tr><th>Input</th><th>Value</th></tr><tr><td>tag</td><td>{input_tag}</td></tr><tr><td>summary</td><td>{input_summary}</td></tr></table></details>\n",  # noqa: E501
        file=f,
    )
    print(f"[Report an issue or request a feature]({r.html_url}/issues)", file=f)


print("✅ \u001b[32;1mFinished Success")


# Commands
# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
# print("::notice::Notice Annotation")
# print("::warning::Warning Annotation")
# print("::error::Error Annotation")
