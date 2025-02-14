
## Setup

```bash
python -m pip install -r requirements.txt
```

For testing purposes, use:
```bash
python -m pip install -r requirements-dev.txt
```

Copy `explain_pr/config.py.sample` to `explain_pr/config.py`, and fill the settings (explained inside the file).


## Set up pre-commits

The first time install the pre commit hooks using:
```bash
pre-commit install
```
Then, it will run automatically when commiting changes.
```

## Run

```bash
python main.py <owner> <repository> <pull_request_id>
```

example (public repository):
```bash
python main.py kartones fg-viewer 24
```

example (public repository, multiple commits editing at least one file two times):
```bash
python main.py kartones bazel-gazelle-sample-web-extension 6
```

## Testing

To run all tests:
```bash
python -m pytest
```

To run a specific test class:
```bash
python -m pytest explain_pr/test/unit/adapters/test_adjusted_pr_for_llm.py
```

To run a specific unit test:
```bash
python -m pytest explain_pr/test/unit/adapters/test_adjusted_pr_for_llm.py::TestAdjustedPullRequestForLlm::test_adjust_patch_data_size_with_pr_smaller_than_limit
```