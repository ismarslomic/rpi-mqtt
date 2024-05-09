> [!NOTE]
> This is markdown documentation of the schema for Settings file. You can find corresponding description as
> JSON schema in [settings.json](settings.json).

# Settings

Model/schema for settings of rpi-mqtt

### Type: `object`

| Property | Type     | Required | Possible values                                         | Deprecated | Default                                                                                                                                                                                                                                                                                                                                                                     | Description                             | Examples |
|----------|----------|----------|---------------------------------------------------------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|----------|
| mqtt     | `object` |          | [MqttSettings](#mqttsettings)                           |            | `{"hostname": "127.0.0.1", "port": 1883, "client_id": "rpi-mqtt", "authentication": null, "tls": null, "base_topic": "home/nodes", "discovery_topic_prefix": "homeassistant", "sensor_name": "rpi-{hostname}"}`                                                                                                                                                             | Settings for the MQTT broker connection |          |
| script   | `object` |          | [ScriptSettings](#scriptsettings)                       |            | `{"update_interval": 60, "log_level": "INFO"}`                                                                                                                                                                                                                                                                                                                              | General settings for this python script |          |
| sensors  | `object` |          | [SensorsMonitoringSettings](#sensorsmonitoringsettings) |            | `{"boot_loader": true, "cpu_use": true, "cpu_load": true, "disk": true, "fan": true, "memory": true, "rpi_model": true, "ip_address": true, "hostname": true, "ethernet_mac_address": true, "wifi_mac_address": true, "wifi_connection": true, "os_kernel": true, "os_release": true, "available_updates": true, "boot_time": true, "temperature": true, "throttle": true}` | Settings for monitoring sensors         |          |

---

# Definitions

## LogLevel

Enum for available log levels

#### Type: `string`

**Possible Values:** `CRITICAL` or `FATAL` or `ERROR` or `WARNING` or `WARNING` or `INFO` or `DEBUG` or `NOTSET`

## MqttAuthentication

Settings for MQTT authentication

#### Type: `object`

| Property | Type     | Required | Possible values | Deprecated | Default | Description                      | Examples |
|----------|----------|----------|-----------------|------------|---------|----------------------------------|----------|
| username | `string` | ✅        | string          |            |         | The MQTT authentication username |          |
| password | `string` | ✅        | string          |            |         | The MQTT authentication password |          |

## MqttSettings

Settings for the MQTT broker connection

#### Type: `object`

| Property               | Type      | Required | Possible values                           | Deprecated | Default            | Description                                                                      | Examples |
|------------------------|-----------|----------|-------------------------------------------|------------|--------------------|----------------------------------------------------------------------------------|----------|
| hostname               | `string`  |          | string                                    |            | `"127.0.0.1"`      | The hostname or IP address of the MQTT broker to connect to                      |          |
| port                   | `integer` |          | integer                                   |            | `1883`             | The TCP port the MQTT broker is listening on                                     |          |
| client_id              | `string`  |          | string                                    |            | `"rpi-mqtt"`       | The ID of this python program to use when connecting to the MQTT broker          |          |
| authentication         | `object`  |          | [MqttAuthentication](#mqttauthentication) |            |                    | The MQTT broker authentication credentials, if required by the broker            |          |
| tls                    | `object`  |          | [MqttTlsSettings](#mqtttlssettings)       |            |                    | The TLS for encrypted connection to the MQTT broker, if supporter by broker      |          |
| base_topic             | `string`  |          | string                                    |            | `"home/nodes"`     | The MQTT base topic under which to publish the Raspberry Pi sensor data topics   |          |
| discovery_topic_prefix | `string`  |          | string                                    |            | `"homeassistant"`  | The prefix for Mqtt Discovery topic subscribed by Home Assistant.                |          |
| sensor_name            | `string`  |          | string                                    |            | `"rpi-{hostname}"` | The MQTT name for this Raspberry Pi as a sensor. Defaults to rpi-<rpi hostname>. |          |

## MqttTlsSettings

Settings for MQTT TLS

#### Type: `object`

| Property | Type     | Required | Possible values | Deprecated | Default | Description                                    | Examples |
|----------|----------|----------|-----------------|------------|---------|------------------------------------------------|----------|
| ca_certs | `string` | ✅        | string          |            |         | Path to the CA Certificate file to verify host |          |
| certfile | `string` | ✅        | string          |            |         | Path to the PEM encoded client certificate     |          |
| keyfile  | `string` | ✅        | string          |            |         | Path to the PEM encoded private key            |          |

## ScriptSettings

General settings for this python script

#### Type: `object`

| Property        | Type      | Required | Possible values       | Deprecated | Default  | Description                                                      | Examples |
|-----------------|-----------|----------|-----------------------|------------|----------|------------------------------------------------------------------|----------|
| update_interval | `integer` |          | integer               |            | `60`     | The interval in seconds to update sensor data to the MQTT broker |          |
| log_level       | `string`  |          | [LogLevel](#loglevel) |            | `"INFO"` | The log level of this python script                              |          |

## SensorsMonitoringSettings

Settings for monitoring sensors

#### Type: `object`

| Property             | Type      | Required | Possible values | Deprecated | Default | Description                            | Examples |
|----------------------|-----------|----------|-----------------|------------|---------|----------------------------------------|----------|
| boot_loader          | `boolean` |          | boolean         |            | `true`  | Enable the bootloader sensor           |          |
| cpu_use              | `boolean` |          | boolean         |            | `true`  | Enable the CPU usage sensor            |          |
| cpu_load             | `boolean` |          | boolean         |            | `true`  | Enable the CPU load sensor             |          |
| disk                 | `boolean` |          | boolean         |            | `true`  | Enable the disk usage sensor           |          |
| fan                  | `boolean` |          | boolean         |            | `true`  | Enable the fan speed sensor            |          |
| memory               | `boolean` |          | boolean         |            | `true`  | Enable the memory usage sensor         |          |
| rpi_model            | `boolean` |          | boolean         |            | `true`  | Enable the Rpi model sensor            |          |
| ip_address           | `boolean` |          | boolean         |            | `true`  | Enable the IP address sensor           |          |
| hostname             | `boolean` |          | boolean         |            | `true`  | Enable the hostname sensor             |          |
| ethernet_mac_address | `boolean` |          | boolean         |            | `true`  | Enable the ethernet mac address sensor |          |
| wifi_mac_address     | `boolean` |          | boolean         |            | `true`  | Enable the wifi mac address sensor     |          |
| wifi_connection      | `boolean` |          | boolean         |            | `true`  | Enable the wifi connection info sensor |          |
| os_kernel            | `boolean` |          | boolean         |            | `true`  | Enable the os kernel sensor            |          |
| os_release           | `boolean` |          | boolean         |            | `true`  | Enable the os release sensor           |          |
| available_updates    | `boolean` |          | boolean         |            | `true`  | Enable the available updates sensor    |          |
| boot_time            | `boolean` |          | boolean         |            | `true`  | Enable the boot time sensor            |          |
| temperature          | `boolean` |          | boolean         |            | `true`  | Enable the temperature sensor          |          |
| throttle             | `boolean` |          | boolean         |            | `true`  | Enable the throttling sensor           |          |
