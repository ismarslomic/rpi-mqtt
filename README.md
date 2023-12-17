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

### Run tests in IntelliJ

In order to run tests easily in IntelliJ you should install the
plugin [pytest imp](https://plugins.jetbrains.com/plugin/14202-pytest-imp).

You should also configure the path to the pyproject.toml in the pytest plugin at _Settings > Tools > Python Integrated
Tools > py.test_
