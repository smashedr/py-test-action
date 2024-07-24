import datetime
import os
from wait import sleep

input_ms = int(os.environ.get('INPUT_MILLISECONDS'))
print(f'input_ms: {input_ms}')

repo = os.environ.get('GITHUB_REPO')
owner = os.environ.get('GITHUB_OWNER')
print(f'repo: {repo}')
print(f'owner: {owner}')

print(f'{datetime.datetime.now().isoformat()}')
result = sleep(input_ms)
print(f'result: {result}')

with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
    print(f'time={result}', file=f)

print('\u001b[32;1mFinished Success.')

# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
# print("::notice::Notice Annotation")
# print("::warning::Warning Annotation")
# print("::error::Error Annotation")
