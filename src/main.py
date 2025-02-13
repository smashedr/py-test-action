import os

print("🏳️ Starting Python Test Action")

input_tag = os.environ.get("INPUT_TAG")
print(f"input_tag: {input_tag}")
input_summary = os.environ.get("INPUT_SUMMARY")
print(f"input_summary: {input_summary}")
input_token = os.environ.get("INPUT_TOKEN")
print(f"input_token: {input_token}")

repo = os.environ.get("GITHUB_REPOSITORY").split("/")[0]
owner = os.environ.get("GITHUB_REPOSITORY").split("/")[1]
print(f"repo: {repo}")
print(f"owner: {owner}")

sha = "WIP"

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    print(f"sha={sha}", file=f)

print("✅ \u001b[32;1mFinished Success")

# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
# print("::notice::Notice Annotation")
# print("::warning::Warning Annotation")
# print("::error::Error Annotation")
