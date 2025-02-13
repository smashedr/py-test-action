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
repository = os.environ.get("GITHUB_REPOSITORY").split("/")[1]
print(f"owner: {owner}")
print(f"repository: {repository}")

sha = os.environ.get("GITHUB_SHA")
print(f"sha: {sha}")


# Action

g = Github(auth=Auth.Token(input_token))
repo = g.get_repo(f"{owner}/{repository}")
print(f"repo.name: {repo.name}")
print(f"repo.full_name: {repo.full_name}")
print(f"repo.git_url: {repo.git_url}")
print(f"repo.git_refs_url: {repo.git_refs_url}")
print(f"repo.git_tags_url: {repo.git_tags_url}")
print(f"repo.html_url: {repo.html_url}")
print(f"repo.releases_url: {repo.releases_url}")

try:
    ref = repo.get_git_ref(f"tags/{input_tag}")
    if ref.object.sha != sha:
        print(f"Updating: {input_tag} -> {ref.object.sha}")
        ref.edit(sha, True)
    else:
        print(f"Unchanged: {input_tag} -> {ref.object.sha}")

except GithubException:
    ref = repo.create_git_ref(f"refs/tags/{input_tag}", sha)
    print(f"Created: {ref.ref} -> {ref.object.sha}")

g.close()


# Outputs

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    print(f"sha={sha}", file=f)


# Summary

with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
    print("### Python Test Action", file=f)
    print(f"Updated: {input_tag} ➡️ `{sha}`", file=f)
    print(f"{repo.html_url}/releases/tag/{input_tag}\n", file=f)
    print(f"[Report an issues or request a feature]({repo.issues_url})", file=f)


print("✅ \u001b[32;1mFinished Success")

# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
# print("::notice::Notice Annotation")
# print("::warning::Warning Annotation")
# print("::error::Error Annotation")
