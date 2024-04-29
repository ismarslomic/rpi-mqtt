#!/usr/bin/env python3
"""Service for reading all Rpi sensors and returning summary of all"""

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from json import JSONEncoder
from typing import List

from sensors.bootloader.sensor import BootloaderSensor
from sensors.bootloader.types import BootloaderVersion
from sensors.cpu.sensor import CpuLoadAvgSensor, CpuUsePctSensor
from sensors.cpu.types import LoadAverage
from sensors.disk.sensor import DiskUseSensor
from sensors.disk.types import DiskUse
from sensors.fan.sensor import FanSpeedSensor
from sensors.fan.types import FanSpeed
from sensors.memory.sensor import MemoryUseSensor
from sensors.memory.types import MemoryUse
from sensors.model.sensor import RpiModelSensor
from sensors.network.sensor import (
    EthernetMacAddressSensor,
    HostnameSensor,
    IpAddressSensor,
    WifiConnectionSensor,
    WifiMacAddressSensor,
)
from sensors.network.types import WiFiConnectionInfo
from sensors.os.sensor import AvailableUpdatesSensor, BootTimeSensor, OsKernelSensor, OsReleaseSensor
from sensors.temperature.sensor import TemperatureSensor
from sensors.temperature.types import HwTemperature
from sensors.throttle.sensor import ThrottledSensor
from sensors.throttle.types import SystemThrottleStatus
from sensors.types import RpiSensor
from settings.types import Settings


@dataclass
class RpiMonitorSummary:
    """Class representing summary of all Rpi monitor sensors"""

    sensors_updated_at: str
    rpi_model: str
    ip: str
    host_name: str
    eth_mac_addr: str
    os_kernel: str
    os_release: str
    booted_at: str
    avail_updates: int
    bootloader_ver: BootloaderVersion
    cpu_use_pct: float
    cpu_load_average: LoadAverage
    disk_usage: DiskUse
    memory_usage: MemoryUse
    fan_spead: dict[str, FanSpeed]
    wifi: WiFiConnectionInfo
    temperature: dict[str, HwTemperature]
    throttle: SystemThrottleStatus


class RpiMonitorSummaryEncoder(JSONEncoder):
    """JSON Encoder to make the summary class JSON serializable"""

    def default(self, o):
        return o.__dict__


def __date_time_now_utc() -> str:
    """Return date time now as string, in UTC with timezone offset. Example: '2024-01-22T18:02:18+00:00'"""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_sensors(settings: Settings) -> RpiMonitorSummary:
    """Read all sensors and return a summary"""

    return RpiMonitorSummary(
        sensors_updated_at=__date_time_now_utc(),
        rpi_model=RpiModelSensor(enabled=settings.sensors.rpi_model).read(),
        ip=IpAddressSensor(enabled=settings.sensors.ip_address).read(),
        host_name=HostnameSensor(enabled=settings.sensors.hostname).read(),
        eth_mac_addr=EthernetMacAddressSensor(enabled=settings.sensors.ethernet_mac_address).read(),
        os_kernel=OsKernelSensor(enabled=settings.sensors.os_kernel).read(),
        os_release=OsReleaseSensor(enabled=settings.sensors.os_release).read(),
        booted_at=BootTimeSensor(enabled=settings.sensors.boot_time).read(),
        avail_updates=AvailableUpdatesSensor(enabled=settings.sensors.available_updates).read(),
        bootloader_ver=BootloaderSensor(enabled=settings.sensors.boot_loader).read(),
        cpu_use_pct=CpuUsePctSensor(enabled=settings.sensors.cpu_use).read(),
        cpu_load_average=CpuLoadAvgSensor(enabled=settings.sensors.cpu_load).read(),
        disk_usage=DiskUseSensor(enabled=settings.sensors.disk).read(),
        memory_usage=MemoryUseSensor(enabled=settings.sensors.memory).read(),
        fan_spead=FanSpeedSensor(enabled=settings.sensors.fan).read(),
        wifi=WifiConnectionSensor(enabled=settings.sensors.wifi_connection).read(),
        temperature=TemperatureSensor(enabled=settings.sensors.temperature).read(),
        throttle=ThrottledSensor(enabled=settings.sensors.throttle).read(),
    )


def print_sensors(settings: Settings) -> None:
    """Print sensors summary as json"""

    all_sensors_json_data = json.dumps(read_sensors(settings), indent=4, cls=RpiMonitorSummaryEncoder)
    print(all_sensors_json_data)


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


def print_sensor_availability(sensors: list[RpiSensor]):
    """Print which sensors are available"""

    for s in sensors:
        print(s.name)
        print(f"Available: {s.available()}")
        if s.available():
            print(f"Value: {s.read()}")

        if hasattr(s, "enabled"):
            print(f"Enabled: {s.enabled()}")
        print()
