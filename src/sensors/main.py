#!/usr/bin/env python3
"""Service for reading all Rpi sensors and returning summary of all"""

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from json import JSONEncoder
from typing import List

from sensors.bootloader.sensor import BootloaderSensor, read_rpi_bootloader_version
from sensors.bootloader.types import BootloaderVersion
from sensors.cpu.sensor import CpuLoadAvgSensor, CpuUsePctSensor, read_cpu_use_percent, read_load_average
from sensors.cpu.types import LoadAverage
from sensors.disk.sensor import DiskUseSensor, read_disk_use
from sensors.disk.types import DiskUse
from sensors.fan.sensor import FanSpeedSensor, read_fans_speed
from sensors.fan.types import FanSpeed
from sensors.memory.sensor import MemoryUseSensor, read_memory_use
from sensors.memory.types import MemoryUse
from sensors.model.sensor import RpiModelSensor, read_rpi_model
from sensors.network.sensor import (
    EthernetMacAddressSensor,
    HostnameSensor,
    IpAddressSensor,
    WifiConnectionSensor,
    WifiMacAddressSensor,
    read_ethernet_mac_address,
    read_hostname,
    read_ip,
    read_wifi_connection,
)
from sensors.network.types import WiFiConnectionInfo
from sensors.os.sensor import (
    AvailableUpdatesSensor,
    BootTimeSensor,
    OsKernelSensor,
    OsReleaseSensor,
    read_number_of_available_updates,
    read_os_release,
    read_rpi_boot_time,
    read_rpi_os_kernel,
)
from sensors.temperature.sensor import TemperatureSensor, read_temperature
from sensors.temperature.types import HwTemperature
from sensors.throttle.sensor import ThrottledSensor, read_throttle_status
from sensors.throttle.types import SystemThrottleStatus
from sensors.types import RpiSensor


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


def read_sensors() -> RpiMonitorSummary:
    """Read all sensors and return a summary"""

    return RpiMonitorSummary(
        sensors_updated_at=__date_time_now_utc(),
        rpi_model=read_rpi_model(),
        ip=read_ip(),
        host_name=read_hostname(),
        eth_mac_addr=read_ethernet_mac_address(),
        os_kernel=read_rpi_os_kernel(),
        os_release=read_os_release(),
        booted_at=read_rpi_boot_time(),
        avail_updates=read_number_of_available_updates(),
        bootloader_ver=read_rpi_bootloader_version(),
        cpu_use_pct=read_cpu_use_percent(),
        cpu_load_average=read_load_average(),
        disk_usage=read_disk_use(),
        memory_usage=read_memory_use(),
        fan_spead=read_fans_speed(),
        wifi=read_wifi_connection(),
        temperature=read_temperature(),
        throttle=read_throttle_status(),
    )


def print_sensors() -> None:
    """Print sensors summary as json"""

    all_sensors_json_data = json.dumps(read_sensors(), indent=4, cls=RpiMonitorSummaryEncoder)
    print(all_sensors_json_data)


def create_sensors() -> List[RpiSensor]:
    """Return a list of all sensors for Rpi"""

    return [
        BootloaderSensor(enabled=False),
        CpuUsePctSensor(enabled=True),
        CpuLoadAvgSensor(enabled=False),
        DiskUseSensor(enabled=True),
        FanSpeedSensor(enabled=False),
        MemoryUseSensor(enabled=True),
        RpiModelSensor(enabled=False),
        IpAddressSensor(enabled=True),
        HostnameSensor(enabled=False),
        EthernetMacAddressSensor(enabled=True),
        WifiMacAddressSensor(enabled=False),
        WifiConnectionSensor(enabled=True),
        OsKernelSensor(enabled=False),
        OsReleaseSensor(enabled=True),
        AvailableUpdatesSensor(enabled=False),
        BootTimeSensor(enabled=True),
        TemperatureSensor(enabled=False),
        ThrottledSensor(enabled=True),
    ]


def print_sensor_availability():
    """Print which sensors are available"""

    all_sensors: list[RpiSensor] = create_sensors()

    for s in all_sensors:
        print(s.name)
        print(f"Available: {s.available()}")
        if s.available():
            print(f"Value: {s.read()}")

        if hasattr(s, "enabled"):
            print(f"Enabled: {s.enabled()}")
        print()


if __name__ == "__main__":
    print_sensor_availability()
