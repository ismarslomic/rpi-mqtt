#!/usr/bin/env python3
"""Service for reading all Rpi sensors and returning summary of all"""

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from json import JSONEncoder

from rpi.bootloader.bootloader import read_rpi_bootloader_version
from rpi.bootloader.types import BootloaderVersion
from rpi.cpu.cpu import read_cpu_use_percent, read_load_average
from rpi.cpu.types import LoadAverage
from rpi.disk.disk import read_disk_use
from rpi.disk.types import DiskUse
from rpi.fan.fan import read_fans_speed
from rpi.fan.types import FanSpeed
from rpi.memory.memory import read_memory_use
from rpi.memory.types import MemoryUse
from rpi.model.model import read_rpi_model
from rpi.network.network import read_ethernet_mac_address, read_hostname, read_ip, read_wifi_connection
from rpi.network.types import WiFiConnectionInfo
from rpi.os.os import read_number_of_available_updates, read_os_release, read_rpi_boot_time, read_rpi_os_kernel
from rpi.temperature.temperature import read_temperature
from rpi.temperature.types import HwTemperature
from rpi.throttle.throttle import read_throttle_status
from rpi.throttle.types import SystemThrottleStatus


@dataclass
class RpiMonitorSummary:
    """Class representing summary of all Rpi monitor sensors"""

    updated_at: str
    rpi_model: str
    ip: str
    host_name: str
    eth_mac: str
    os_kernel: str
    os_release: str
    booted_at: str
    avail_updates: int
    bootloader_ver: BootloaderVersion
    cpu_use_pct: float
    cpu_load_average: LoadAverage
    disk_usage: DiskUse
    memory_usage: MemoryUse
    fan_spead: list[FanSpeed]
    wifi_connection_ip: WiFiConnectionInfo
    temperature: list[HwTemperature]
    throttle_status: SystemThrottleStatus


class RpiMonitorSummaryEncoder(JSONEncoder):
    """JSON Encoder to make the summary class JSON serializable"""

    def default(self, o):
        return o.__dict__


def __date_time_now_utc() -> str:
    """Return date time now as string, in UTC with timezone offset. Example: '2024-01-22T18:02:18+00:00'"""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


monitor_summary = RpiMonitorSummary(
    updated_at=__date_time_now_utc(),
    rpi_model=read_rpi_model(),
    ip=read_ip(),
    host_name=read_hostname(),
    eth_mac=read_ethernet_mac_address(),
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
    wifi_connection_ip=read_wifi_connection(),
    temperature=read_temperature(),
    throttle_status=read_throttle_status(),
)

all_sensors_json_data = json.dumps(monitor_summary, indent=4, cls=RpiMonitorSummaryEncoder)
print(all_sensors_json_data)
