# Raspberry Pi - Mqtt pub/sub client

## Python Modules

- `mqtt.pub` - utilities for publishing Rpi sensors to MQTT topics
- `mqtt.sub` - utilities for subscribing to MQTT topics
- `sensors` - modules to read Rpi sensor data

## Installation

### Experimenting with nix
```shell
# Install nix, see https://nixos.org/download/#nix-install-linux
$ sh <(curl -L https://nixos.org/nix/install) --daemon

# Create nix shell
nix-shell
```

```bash
# Clone this git repo
git clone https://github.com/ismarslomic/rpi-mqtt.git
cd rpi-mqtt

# Create python virtual environment (required in Bookworm)
python3 -m venv --system-site-packages .venv
source .venv/bin/activate

# Install poetry
pip3 install poetry

# Disable keyring, otherwise poetry will be hanging
keyring --disable

# Install required python packages defined in pyproject.toml
poetry install --without dev --no-root
```

## Usage

```bash
# Run python program
cd src
python3 -m sensors.main -s /Users/john/rpi-mqtt/settings.yml
```

You can provide user settings by providing a `settings.yml` file according to the JSON
schema [settings.json](docs/settings.json) or markdown [settings.md](docs/settings.md).

Example `settings.yml`:

```yaml
mqtt:
  # The hostname or IP address of the MQTT broker to connect to. Default 127.0.0.1.
  hostname: 127.0.0.1
  # The TCP port the MQTT broker is listening on. Default: 1883.
  port: 1883
  # Override the default sensor_name (rpi-<hostname>) with own name of sensor to be used in MQTT topic name.
  sensor_name: my-macbook

script:
  # The interval to update sensor data to MQTT broker. In seconds. Default: 60.
  update_interval: 120
  # The log level for the python script. Default: INFO.
  log_level: DEBUG

# Override default settings by enabling (true) or disabling (false) sensors you want to be published to MQTT broker
sensors:
  boot_loader: False
  cpu: True
  disk: True
  fan: False
```

## Development

Read [DEVELOPMENT.md](DEVELOPMENT.md) for more information about how to contribute.
