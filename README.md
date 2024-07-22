[![Tags](https://img.shields.io/github/actions/workflow/status/smashedr/py-test-action/tags.yaml?logo=github&logoColor=white&label=tags)](https://github.com/smashedr/py-test-action/actions/workflows/tags.yaml)
[![Test](https://img.shields.io/github/actions/workflow/status/smashedr/py-test-action/test.yaml?logo=github&logoColor=white&label=test)](https://github.com/smashedr/py-test-action/actions/workflows/test.yaml)
[![GitHub Release Version](https://img.shields.io/github/v/release/smashedr/py-test-action?logo=github)](https://github.com/smashedr/py-test-action/releases/latest)
[![GitHub Top Language](https://img.shields.io/github/languages/top/smashedr/py-test-action?logo=htmx&logoColor=white)](https://github.com/smashedr/py-test-action)
[![GitHub Org Stars](https://img.shields.io/github/stars/cssnr?style=flat&logo=github&logoColor=white)](https://cssnr.github.io/)
[![Discord](https://img.shields.io/discord/899171661457293343?logo=discord&logoColor=white&label=discord&color=7289da)](https://discord.gg/wXy6m2X8wY)

# Python Test Action

* [Inputs](#Inputs)
* [Outputs](#Outputs)

## Inputs

| input | required | default | description                     |
|-------|----------|---------|---------------------------------|
| url   | **Yes**  | -       | URL with `{ref}` in the string. |

```yaml
  - name: "Mozilla Addon Update"
    uses: smashedr/py-test-action@master
    with:
      url: "https://example.com/?ref={ref}"
```

## Outputs

| output | description       |
|--------|-------------------|
| url    | Update URL Result |

```yaml
  - name: "PY Test Action"
    id: update
    uses: smashedr/py-test-action@master
    with:
      url: "https://example.com/?ref={ref}"

  - name: "Echo Output"
    run: |
      echo '${{ steps.update.outputs.url }}'
```
