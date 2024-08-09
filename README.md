
## Setup

```bash
python3 -m pip install -r requirements.txt
```

Copy `explain_pr/config.py.sample` to `explain_pr/config.py`, and fill the settings (explained inside the file).

## run

```bash
python3 main.py <owner> <repository> <pull_request_id>
```

example (public repository):
```bash
python3 main.py kartones fg-viewer 24
```

example (public repository, multiple commits editing at least one file two times):
```bash
python3 main.py kartones bazel-gazelle-sample-web-extension 6
```


# TODO:

https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api?apiVersion=2022-11-28
example: https://github.com/Kartones/fg-viewer/pull/24/files