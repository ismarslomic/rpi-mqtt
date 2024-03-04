> [!NOTE]
> This is markdown documentation of the schema for Settings file. You can find corresponding description as
> JSON schema in [settings.json](settings.json).

# Settings

Model/schema for settings of rpi-mqtt

| Property | Type | Required | Possible Values | Deprecated | Default | Description | Examples
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | --------
| mqtt | `object` |  | [MqttSettings](#mqttsettings)|  | `{"hostname": "127.0.0.1", "port": 1883, "client_id": "rpi-mqtt", "authentication": null, "tls": null}` | Settings for the MQTT broker connection | |
| script | `object` |  | [ScriptSettings](#scriptsettings)|  | `{"update_interval": 60}` | General settings for this python script | |
| sensors | `object` |  | [SensorsMonitoringSettings](#sensorsmonitoringsettings)|  | `{"boot_loader": true, "cpu": true, "disk": true, "fan": true, "memory": true, "network": true, "os": true, "temperature": true, "throttle": true}` | Settings for monitoring sensors | |


---

# Definitions



## MqttAuthentication

Settings for MQTT authentication

### Type: `object`

| Property | Type | Required | Possible Values | Deprecated | Default | Description | Examples
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | --------
| username | `string` | ✅ | string|  |  | The MQTT authentication username | |
| password | `string` | ✅ | string|  |  | The MQTT authentication password | |


## MqttSettings

Settings for the MQTT broker connection

### Type: `object`

| Property | Type | Required | Possible Values | Deprecated | Default | Description | Examples
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | --------
| hostname | `string` |  | string|  | `"127.0.0.1"` | The hostname or IP address of the MQTT broker to connect to | |
| port | `integer` |  | integer|  | `1883` | The TCP port the MQTT broker is listening on | |
| client_id | `string` |  | string|  | `"rpi-mqtt"` | The ID of this python program to use when connecting to the MQTT broker | |
| authentication | `object` |  | [MqttAuthentication](#mqttauthentication)|  |  | The MQTT broker authentication credentials, if required by the broker | |
| tls | `object` |  | [MqttTlsSettings](#mqtttlssettings)|  |  | The TLS for encrypted connection to the MQTT broker, if supporter by broker | |


## MqttTlsSettings

Settings for MQTT TLS

### Type: `object`

| Property | Type | Required | Possible Values | Deprecated | Default | Description | Examples
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | --------
| ca_certs | `string` | ✅ | string|  |  | Path to the CA Certificate file to verify host | |
| certfile | `string` | ✅ | string|  |  | Path to the PEM encoded client certificate | |
| keyfile | `string` | ✅ | string|  |  | Path to the PEM encoded private key | |


## ScriptSettings

General settings for this python script

### Type: `object`

| Property | Type | Required | Possible Values | Deprecated | Default | Description | Examples
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | --------
| update_interval | `integer` |  | integer|  | `60` | The interval to update sensor data to the MQTT broker | |


## SensorsMonitoringSettings

Settings for monitoring sensors

### Type: `object`

| Property | Type | Required | Possible Values | Deprecated | Default | Description | Examples
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | --------
| boot_loader | `boolean` |  | boolean|  | `true` | Enable monitoring of the boot loader | |
| cpu | `boolean` |  | boolean|  | `true` | Enable monitoring of the CPU | |
| disk | `boolean` |  | boolean|  | `true` | Enable monitoring of the disk | |
| fan | `boolean` |  | boolean|  | `true` | Enable monitoring of the fan | |
| memory | `boolean` |  | boolean|  | `true` | Enable monitoring of the memory | |
| network | `boolean` |  | boolean|  | `true` | Enable monitoring of the network | |
| os | `boolean` |  | boolean|  | `true` | Enable monitoring of the os | |
| temperature | `boolean` |  | boolean|  | `true` | Enable monitoring of the temperatures | |
| throttle | `boolean` |  | boolean|  | `true` | Enable monitoring of the throttling | |
