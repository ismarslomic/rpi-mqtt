#!/usr/bin/env python3
"""Class responsible for publishing messages to the MQTT broker"""

import _thread
import json
import logging
from collections import OrderedDict
from time import sleep

from paho.mqtt.client import Client, MQTTMessageInfo

from mqtt.types import RpiMqttTopics
from sensors.types import AllRpiSensors


class RpiMqttPublisher:
    """Class responsible for publishing messages to the MQTT broker"""

    _logger: logging.Logger
    mqtt_client: Client
    mqtt_topics: RpiMqttTopics
    all_sensors: AllRpiSensors
    PAYLOAD_LWT_ONLINE = "online"
    PAYLOAD_LWT_OFFLINE = "offline"

    def __init__(self, mqtt_client: Client, mqtt_topics: RpiMqttTopics, all_sensors: AllRpiSensors):
        self._logger = logging.getLogger(__name__)
        self.mqtt_client = mqtt_client
        self.mqtt_topics = mqtt_topics
        self.all_sensors = all_sensors

    def pub_online_lwt(self):
        """Publish online LWT status message for all lwt topics"""

        for lwt_topic in self.mqtt_topics.lwt_topic_names:
            self.mqtt_client.publish(lwt_topic, payload=self.PAYLOAD_LWT_ONLINE, retain=False)
            self._logger.info("Published '%s' lwt message to MQTT topic '%s'", self.PAYLOAD_LWT_ONLINE, lwt_topic)

    def pub_offline_lwt(self):
        """Publish offline LWT status message for all lwt topics"""

        # Handle cases where we have lost connection to the broker, but need to exit
        if not self.mqtt_client.is_connected():
            return

        wait_timeout_seconds = 2

        for lwt_topic in self.mqtt_topics.lwt_topic_names:
            msg_info: MQTTMessageInfo = self.mqtt_client.publish(
                lwt_topic, payload=self.PAYLOAD_LWT_OFFLINE, retain=False
            )
            msg_info.wait_for_publish(timeout=wait_timeout_seconds)
            self._logger.info("Published '%s' lwt message to MQTT topic '%s'", self.PAYLOAD_LWT_OFFLINE, lwt_topic)

    def pub_sensor_updates(self, refresh_sensors: bool = True):
        """Publish updated sensor values to broker"""

        if refresh_sensors:
            self.all_sensors.refresh_available_sensors()

        sensor_data: OrderedDict = self.all_sensors.as_dict()
        _thread.start_new_thread(self._pub_sensor_updates, (sensor_data,))

        self._logger.info("Publishing updated sensor data")

    def _pub_sensor_updates(self, payload: OrderedDict):
        self.mqtt_client.publish(
            topic=self.mqtt_topics.sensor_states_topic, payload=json.dumps(payload), qos=1, retain=False
        )
        sleep(0.5)  # some slack for the publishing roundtrip and callback function
