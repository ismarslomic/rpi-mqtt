#!/usr/bin/env python3
"""Service for reading all Rpi sensors and returning summary of all"""

from collections import OrderedDict
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
from settings.types import Settings


def create_sensors(settings: Settings) -> List[RpiSensor]:
    """Return a list of all sensors for Rpi"""

    return [
        BootloaderSensor(enabled=settings.sensors.boot_loader),
        CpuUsePctSensor(enabled=settings.sensors.cpu_use),
        CpuLoadAvgSensor(enabled=settings.sensors.cpu_load),
        DiskUseSensor(enabled=settings.sensors.disk),
        FanSpeedSensor(enabled=settings.sensors.fan),
        MemoryUseSensor(enabled=settings.sensors.memory),
        RpiModelSensor(enabled=settings.sensors.rpi_model),
        IpAddressSensor(enabled=settings.sensors.ip_address),
        HostnameSensor(enabled=settings.sensors.hostname),
        EthernetMacAddressSensor(enabled=settings.sensors.ethernet_mac_address),
        WifiMacAddressSensor(enabled=settings.sensors.wifi_mac_address),
        WifiConnectionSensor(enabled=settings.sensors.wifi_connection),
        OsKernelSensor(enabled=settings.sensors.os_kernel),
        OsReleaseSensor(enabled=settings.sensors.os_release),
        AvailableUpdatesSensor(enabled=settings.sensors.available_updates),
        BootTimeSensor(enabled=settings.sensors.boot_time),
        TemperatureSensor(enabled=settings.sensors.temperature),
        ThrottledSensor(enabled=settings.sensors.throttle),
    ]


class AllRpiSensors:
    """Class representing all sensors"""

    # pylint: disable=R0903

    sensors: List[RpiSensor]

    def __init__(self, sensors: List[RpiSensor]):
        self.sensors = sensors

    def as_dict(self) -> OrderedDict:
        """Sensor states as ordered dict"""
        sensors_as_dict: OrderedDict = OrderedDict()
        for sensor in self.sensors:
            if sensor.available():
                sensors_as_dict[sensor.name] = sensor.refresh_state()
        return sensors_as_dict


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
