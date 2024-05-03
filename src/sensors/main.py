#!/usr/bin/env python3
"""Service for reading all Rpi sensors and returning summary of all"""

from typing import List

from sensors.bootloader.sensor import BootloaderSensor
from sensors.cpu.sensor import CpuLoadAvgSensor, CpuUsePctSensor
from sensors.disk.sensor import DiskUseSensor
from sensors.fan.sensor import FanSpeedSensor
from sensors.memory.sensor import MemoryUseSensor
from sensors.model.sensor import RpiModelSensor
from sensors.network.sensor import (
    EthernetMacAddressSensor,
    HostnameSensor,
    IpAddressSensor,
    WifiConnectionSensor,
    WifiMacAddressSensor,
)
from sensors.os.sensor import AvailableUpdatesSensor, BootTimeSensor, OsKernelSensor, OsReleaseSensor
from sensors.temperature.sensor import TemperatureSensor
from sensors.throttle.sensor import ThrottledSensor
from sensors.types import RpiSensor
from settings.types import SensorsMonitoringSettings


def create_sensors(sensor_settings: SensorsMonitoringSettings) -> List[RpiSensor]:
    """Return a list of all sensors for Rpi"""

    return [
        BootloaderSensor(enabled=sensor_settings.boot_loader),
        CpuUsePctSensor(enabled=sensor_settings.cpu_use),
        CpuLoadAvgSensor(enabled=sensor_settings.cpu_load),
        DiskUseSensor(enabled=sensor_settings.disk),
        FanSpeedSensor(enabled=sensor_settings.fan),
        MemoryUseSensor(enabled=sensor_settings.memory),
        RpiModelSensor(enabled=sensor_settings.rpi_model),
        IpAddressSensor(enabled=sensor_settings.ip_address),
        HostnameSensor(enabled=sensor_settings.hostname),
        EthernetMacAddressSensor(enabled=sensor_settings.ethernet_mac_address),
        WifiMacAddressSensor(enabled=sensor_settings.wifi_mac_address),
        WifiConnectionSensor(enabled=sensor_settings.wifi_connection),
        OsKernelSensor(enabled=sensor_settings.os_kernel),
        OsReleaseSensor(enabled=sensor_settings.os_release),
        AvailableUpdatesSensor(enabled=sensor_settings.available_updates),
        BootTimeSensor(enabled=sensor_settings.boot_time),
        TemperatureSensor(enabled=sensor_settings.temperature),
        ThrottledSensor(enabled=sensor_settings.throttle),
    ]


def print_sensor_availability(sensors: list[RpiSensor]):
    """Print which sensors are available"""

    for s in sensors:
        print(s.name)
        print(f"Available: {s.available()}")
        if s.available():
            print(f"Value: {s.refresh_state()}")

        if hasattr(s, "enabled"):
            print(f"Enabled: {s.enabled()}")
        print()
