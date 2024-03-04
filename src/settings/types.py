#!/usr/bin/env python3
"""Types in module Settings"""

from typing import Optional

from pydantic import BaseModel, Field


class MqttAuthentication(BaseModel):
    """Settings for MQTT authentication"""

    username: str = Field(description="The MQTT authentication username")
    password: str = Field(description="The MQTT authentication password")


class MqttTlsSettings(BaseModel):
    """Settings for MQTT TLS"""

    ca_certs: str = Field(description="Path to the CA Certificate file to verify host")
    certfile: str = Field(description="Path to the PEM encoded client certificate")
    keyfile: str = Field(description="Path to the PEM encoded private key")


class MqttSettings(BaseModel):
    """Settings for the MQTT broker connection"""

    hostname: str = Field(
        default="127.0.0.1", description="The hostname or IP address of the MQTT broker to connect to"
    )
    port: int = Field(default=1883, description="The TCP port the MQTT broker is listening on")
    client_id: str = Field(
        default="rpi-mqtt", description="The ID of this python program to use when connecting to the MQTT broker"
    )
    authentication: Optional[MqttAuthentication] = Field(
        default=None, description="The MQTT broker authentication credentials, if required by the broker"
    )
    tls: Optional[MqttTlsSettings] = Field(
        default=None, description="The TLS for encrypted connection to the MQTT broker, if supporter by broker"
    )


class ScriptSettings(BaseModel):
    """General settings for this python script"""

    update_interval: int = Field(default=60, description="The interval to update sensor data to the MQTT broker")


class SensorsMonitoringSettings(BaseModel):
    """Settings for monitoring sensors"""

    boot_loader: bool = Field(default=True, description="Enable monitoring of the boot loader")
    cpu: bool = Field(default=True, description="Enable monitoring of the CPU")
    disk: bool = Field(default=True, description="Enable monitoring of the disk")
    fan: bool = Field(default=True, description="Enable monitoring of the fan")
    memory: bool = Field(default=True, description="Enable monitoring of the memory")
    network: bool = Field(default=True, description="Enable monitoring of the network")
    os: bool = Field(default=True, description="Enable monitoring of the os")
    temperature: bool = Field(default=True, description="Enable monitoring of the temperatures")
    throttle: bool = Field(default=True, description="Enable monitoring of the throttling")


class Settings(BaseModel):
    """Model/schema for settings of rpi-mqtt"""

    mqtt: MqttSettings = Field(description="Settings for the MQTT broker connection", default=MqttSettings())
    script: ScriptSettings = Field(description="General settings for this python script", default=ScriptSettings())
    sensors: SensorsMonitoringSettings = Field(
        description="Settings for monitoring sensors", default=SensorsMonitoringSettings()
    )
