import os
from github import Github, Auth

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

user = g.get_user()
print(f"user.login: {user.login}")

repo = g.get_repo(f"{owner}/{repo}")
print(f"repo.name: {repo.name}")

try:
    ref = repo.get_git_ref(f"refs/tags/{input_tag}")
    print(f"ref: {ref}")
    print(f"ref.ref: {ref.ref}")
    print(f"ref.object: {ref.object}")
    print(f"ref.object.sha: {ref.object.sha}")
    if ref.object.sha != sha:
        print(f"Updating: {input_tag}")
        ref.edit(sha, True)
    else:
        print(f"Unchanged: {input_tag}")

except Exception:
    print(f"Ref not found: {input_tag}")
    print(f"Creating: {input_tag}")
    ref = repo.create_git_ref(f"refs/tags/{input_tag}", sha)
    print(f"ref: {ref}")
    print(f"ref.ref: {ref.ref}")
    print(f"ref.object: {ref.object}")
    print(f"ref.object.sha: {ref.object.sha}")

# To close connections after use
g.close()


# Outputs

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    print(f"sha={sha}", file=f)

print("✅ \u001b[32;1mFinished Success")

# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
# print("::notice::Notice Annotation")
# print("::warning::Warning Annotation")
# print("::error::Error Annotation")
