#!/usr/bin/env python3
"""Types in module Settings"""
from enum import Enum
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
    base_topic: Optional[str] = Field(
        default="home/nodes",
        description="The MQTT base topic under which to publish the Raspberry Pi sensor data topics",
    )
    sensor_name: Optional[str] = Field(
        default="rpi-{hostname}",
        description="The MQTT name for this Raspberry Pi as a sensor. Defaults to rpi-<rpi hostname>.",
    )


class LogLevel(str, Enum):
    """Enum for available log levels"""

    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARN = "WARNING"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


class ScriptSettings(BaseModel):
    """General settings for this python script"""

    update_interval: int = Field(
        default=60, description="The interval in seconds to update sensor data to the MQTT broker"
    )
    log_level: LogLevel = Field(default=LogLevel.INFO, description="The log level of this python script")


class SensorsMonitoringSettings(BaseModel):
    """Settings for monitoring sensors"""

    boot_loader: bool = Field(default=True, description="Enable the bootloader sensor")
    cpu_use: bool = Field(default=True, description="Enable the CPU usage sensor")
    cpu_load: bool = Field(default=True, description="Enable the CPU load sensor")
    disk: bool = Field(default=True, description="Enable the disk usage sensor")
    fan: bool = Field(default=True, description="Enable the fan speed sensor")
    memory: bool = Field(default=True, description="Enable the memory usage sensor")
    rpi_model: bool = Field(default=True, description="Enable the Rpi model sensor")
    ip_address: bool = Field(default=True, description="Enable the IP address sensor")
    hostname: bool = Field(default=True, description="Enable the hostname sensor")
    ethernet_mac_address: bool = Field(default=True, description="Enable the ethernet mac address sensor")
    wifi_mac_address: bool = Field(default=True, description="Enable the wifi mac address sensor")
    wifi_connection: bool = Field(default=True, description="Enable the wifi connection info sensor")
    os_kernel: bool = Field(default=True, description="Enable the os kernel sensor")
    os_release: bool = Field(default=True, description="Enable the os release sensor")
    available_updates: bool = Field(default=True, description="Enable the available updates sensor")
    boot_time: bool = Field(default=True, description="Enable the boot time sensor")
    temperature: bool = Field(default=True, description="Enable the temperature sensor")
    throttle: bool = Field(default=True, description="Enable the throttling sensor")


class Settings(BaseModel):
    """Model/schema for settings of rpi-mqtt"""

    mqtt: MqttSettings = Field(default=MqttSettings(), description="Settings for the MQTT broker connection")
    script: ScriptSettings = Field(default=ScriptSettings(), description="General settings for this python script")
    sensors: SensorsMonitoringSettings = Field(
        default=SensorsMonitoringSettings(), description="Settings for monitoring sensors"
    )
