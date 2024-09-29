#!/usr/bin/env python3
"""Service for reading the Rpi bootloader version"""

import subprocess
from typing import List

from mqtt.constants import PAYLOAD_LWT_OFFLINE, PAYLOAD_LWT_ONLINE
from mqtt.types import RpiMqttTopics
from sensors.bootloader.types import BootloaderVersion
from sensors.types import MqttDiscoveryEntity, MqttDiscoveryMessage, RpiSensor, SensorNotAvailableException
from sensors.utils import date_and_timestamp_to_iso_datetime


class BootloaderSensor(RpiSensor):
    """Sensor for bootloader version"""

    _state: BootloaderVersion | None = None

    @property
    def name(self) -> str:
        return "bootloader_version"

    @property
    def state(self) -> BootloaderVersion | None:
        return self._state

    # pylint: disable=R0801
    # noinspection DuplicatedCode
    # TODO: clean up the duplicated code
    def mqtt_discovery_messages(self, topics: RpiMqttTopics) -> List[MqttDiscoveryMessage]:
        binary_sensor = MqttDiscoveryEntity(
            name="Bootloader update",
            unique_id="rpi_bootloader_update",
            component="binary_sensor",
            device_class="update",
            value_template=f"{{{{ value_json.{self.name}.status }}}}",
            base_topic=topics.sensor_states_base_topic,
            state_topic=topics.sensor_states_topic_abbr,
            availability_topic=topics.sensor_states_lwt_topic_abbr,
            payload_available=PAYLOAD_LWT_ONLINE,
            payload_not_available=PAYLOAD_LWT_OFFLINE,
            payload_on="update available",
            payload_off="up to date",
            json_attributes_topic=topics.sensor_states_topic_abbr,
            json_attributes_template=f"{{{{ value_json.{self.name} | tojson }}}}",
        )

        binary_sensor_dict: dict = vars(binary_sensor)

        # Rename 'base_topic' with '~'
        binary_sensor_dict["~"] = binary_sensor_dict["base_topic"]
        del binary_sensor_dict["base_topic"]

        # Remove None values
        for k, v in list(binary_sensor_dict.items()):
            if v is None:
                del binary_sensor_dict[k]

        discovery_topic: str = topics.discovery_topic(
            component=binary_sensor.component, unique_id=binary_sensor.unique_id
        )

        discovery_messages: List[MqttDiscoveryMessage] = [
            MqttDiscoveryMessage(payload=binary_sensor_dict, topic=discovery_topic)
        ]

        return discovery_messages

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_rpi_bootloader_version()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_rpi_bootloader_version(self) -> BootloaderVersion:
        """Read current Rpi bootloader version and check for updates"""

        # doc: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#updating-the-eeprom-configuration
        args = ["rpi-eeprom-update"]

        try:
            result = subprocess.run(args, capture_output=True, text=True, check=False)
        except FileNotFoundError as err:
            self.logger.warning("Failed calling process rpi-eeprom-update: %s", str(err))
            raise SensorNotAvailableException("rpi-eeprom-update not available for this Rpi") from err

        if result.returncode != 0:
            self.logger.warning(
                "Process 'rpi-eeprom-update' returned code %s: %s", str(result.returncode), str(result.stderr)
            )
            raise SensorNotAvailableException("Failed to read Rpi bootloader version", result.stderr)

        result_as_list = result.stdout.split("\n")

        update_status = ""
        current_version = ""
        latest_version = ""

        for item in result_as_list:
            item_stripped = item.strip()
            if update_status == "" and item_stripped.startswith("BOOTLOADER:"):
                item_split = item_stripped.split("BOOTLOADER: ")
                update_status = item_split[1].strip()
            elif current_version == "" and item_stripped.startswith("CURRENT:"):
                item_split = item_stripped.split("CURRENT: ")
                current_version = date_and_timestamp_to_iso_datetime(item_split[1].strip())
            elif latest_version == "" and item_stripped.startswith("LATEST:"):
                item_split = item_stripped.split("LATEST: ")
                latest_version = date_and_timestamp_to_iso_datetime(item_split[1].strip())

        return BootloaderVersion(status=update_status, current=current_version, latest=latest_version)
