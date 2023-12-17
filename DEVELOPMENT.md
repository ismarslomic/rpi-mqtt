# Development

Run main script that publish and subscribes to MQTT

```bash
poetry run pub-sub
```

Install [pyenv](https://github.com/pyenv/pyenv#homebrew-in-macos)

```bash
brew update
brew install pyenv
```

Install [poetry](https://python-poetry.org/docs/)

```bash
brew update
brew install pipx
pipx install poetry
```

Upgrade poetry

```bash
pipx upgrade poetry
```

Start shell

```bash
poetry shell
```

Install all dependencies (_main_ and _dev_)

```bash
poetry install
```

Install _main_ dependencies only

```bash
poetry install --only main
```

Install [git hooks scripts](https://pre-commit.com)

```bash
pre-commit install
```

Add _main_ package

```bash
poetry add <package>
```

Add _dev_ package

```bash
poetry add <package> --group dev
```

Update all dependencies to latest version

```bash
poetry update
```

## Testing

### Run tests in command line

[pytest](https://docs.pytest.org/en/latest/) is used as test framework.

```bash
poetry run pytest
```

### Create test coverage

[pytest-cov](https://pypi.org/project/pytest-cov/) is used to produce test coverage reports.

```bash
poetry run coverage run -m pytest -vv && poetry run coverage report
```

### Run tests in IntelliJ

In order to run tests easily in IntelliJ you should install the
plugin [pytest imp](https://plugins.jetbrains.com/plugin/14202-pytest-imp).

You should also configure the path to the pyproject.toml in the pytest plugin at _Settings > Tools > Python Integrated
Tools > py.test_

## Code style

[Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) is used as code
style.

You can do a style check, without fixing the issues:

```bash
poetry run black src tests --check --diff
```

or fix the issues automatically:

```bash
poetry run black src tests
```

## Static code analysis

[Pylint](https://pylint.pycqa.org/en/latest/) is used for static code analysis.

```bash
poetry run pylint src
```

## Import ordering

[isort](https://pycqa.github.io/isort/) is used to verify import ordering.

You can do a check, without fixing the issues:

```bash
poetry run isort src tests --check --diff
```

or fix the issues automatically:

```bash
poetry run isort src tests
```
