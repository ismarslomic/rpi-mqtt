# Raspberry Pi - Mqtt pub/sub client

## Python Modules

- `mqtt.pub` - utilities for publishing to MQTT topics
- `mqtt.sub` - utilities for subscribing to MQTT topics

## Development

Run main script that publish and subscribes to MQTT

```bash
poetry run pub-sub
```

Start shell

```bash
poetry shell
```

Install dependencies

```bash
poetry install
```

Install package

```bash
poetry add <package>
```

Install dev package

```bash
poetry add --dev <package>
```

Update all dependencies to latest version

```bash
poetry update
```

## Testing

### Run tests in command line

```bash
poetry run pytest
```

### Run tests in IntelliJ

In order to run tests easily in IntelliJ you should install the
plugin [pytest imp](https://plugins.jetbrains.com/plugin/14202-pytest-imp).

You should also configure the path to the pyproject.toml in the pytest plugin at _Settings > Tools > Python Integrated
Tools > py.test_

## Code style

This repo use [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) for
Python.

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
