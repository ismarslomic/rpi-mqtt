#!/usr/bin/env python3
"""Service for reading all Rpi sensors and returning summary of all"""

from collections import OrderedDict
from typing import List

from date_utils import now_to_iso_datetime
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
from settings.types import ScriptSettings, Settings


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

    sensors: List[RpiSensor]
    update_interval: int
    sensors_total: int = 0
    sensors_available: int = 0

    def __init__(self, sensors: List[RpiSensor], script_settings: ScriptSettings):
        self.sensors = sensors
        self.update_interval = script_settings.update_interval
        self.sensors_total = len(self.sensors)

    def metadata(self) -> dict[str, str | int]:
        """Returns dictionary with metadata properties"""
        return {
            "states_refresh_ts": now_to_iso_datetime(),
            "update_interval": self.update_interval,
            "sensors_total": self.sensors_total,
            "sensors_available": self.sensors_available,
        }

    def as_dict(self) -> OrderedDict:
        """Sensor states as ordered dict"""

        sensors_as_dict: OrderedDict = OrderedDict()
        self.sensors_available = 0

        # Loop all sensors and add to ordered dictionary
        for sensor in self.sensors:
            if sensor.available():
                self.sensors_available += 1
                sensor.refresh_state()
                sensors_as_dict[sensor.name] = sensor.state_as_dict

        # Add metadata properties
        sensors_as_dict["metadata"] = self.metadata()

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
