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
repo = g.get_repo(f"{owner}/{repo}")
print(f"repo.name: {repo.name}")
print(f"repo.full_name: {repo.full_name}")

try:
    ref = repo.get_git_ref(f"refs/tags/{input_tag}")
    print(f"ref.ref: {ref.ref}")
    print(f"ref.object.sha: {ref.object.sha}")
    if ref.object.sha != sha:
        print(f"Updating: {input_tag}")
        ref.edit(sha, True)
    else:
        print(f"Unchanged: {input_tag}")

except GithubException:
    print(f"Ref not found: {input_tag}")
    print(f"Creating: {input_tag}")
    ref = repo.create_git_ref(f"refs/tags/{input_tag}", sha)
    print(f"ref.ref: {ref.ref}")
    print(f"ref.object.sha: {ref.object.sha}")

g.close()


# Outputs

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    print(f"sha={sha}", file=f)


# Summary

with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
    print("### Python Test Action", file=f)
    print(f"Updated: {input_tag} ➡️ `{sha}`", file=f)
    print(f"https://github.com/{owner}/{repo}/releases/tag/{input_tag}", file=f)


print("✅ \u001b[32;1mFinished Success")

# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
# print("::notice::Notice Annotation")
# print("::warning::Warning Annotation")
# print("::error::Error Annotation")
