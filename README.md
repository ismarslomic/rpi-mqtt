# Raspberry Pi - Mqtt pub/sub client

## Python Modules

- `mqtt.pub` - utilities for publishing Rpi sensors to MQTT topics
- `mqtt.sub` - utilities for subscribing to MQTT topics
- `rpi` - utilities for reading Rpi sensors

## Installation
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

# Run python program
cd src
python3 -m rpi.main
```


## Development
Read [DEVELOPMENT.md](DEVELOPMENT.md) for more information about how to contribute.
