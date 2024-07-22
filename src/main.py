import os

input_url = os.environ.get('INPUT_URL')
print(f'Processing URL: {input_url}')

ref_name = os.environ.get('GITHUB_REF_NAME')
print(f'Using GITHUB_REF_NAME: {ref_name}')

url = input_url.format(ref=ref_name)
print(f'Updated URL: {url}')

# https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/
# print(f'::set-output name=url::{url}')
# print(f'::set-output name=result::{json.dumps(result)}')

# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
    print(f'url={url}', file=f)

# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
# print("::notice::Notice Annotation")
# print("::warning::Warning Annotation")
# print("::error::Error Annotation")

print('\u001b[32;1mFinished Success.')
