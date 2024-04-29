#!/usr/bin/env python3
"""Class responsible for publishing messages to the MQTT broker"""

import logging

from paho.mqtt.client import Client, MQTTMessageInfo


class RpiMqttPublisher:
    """Class responsible for publishing messages to the MQTT broker"""

    _logger: logging.Logger
    mqtt_client: Client
    lwt_topics: list[str]
    PAYLOAD_LWT_ONLINE = "online"
    PAYLOAD_LWT_OFFLINE = "offline"

    def __init__(self, mqtt_client: Client, lwt_topics: list[str]):
        self._logger = logging.getLogger(__name__)
        self.mqtt_client = mqtt_client
        self.lwt_topics = lwt_topics

    def pub_online_lwt(self):
        """Publish online LWT status message for all lwt topics"""

        for lwt_topic in self.lwt_topics:
            self.mqtt_client.publish(lwt_topic, payload=self.PAYLOAD_LWT_ONLINE, retain=False)
            self._logger.info("Published '%s' lwt message to MQTT topic '%s'", self.PAYLOAD_LWT_ONLINE, lwt_topic)

    def pub_offline_lwt(self):
        """Publish offline LWT status message for all lwt topics"""

        # Handle cases where we have lost connection to the broker, but need to exit
        if not self.mqtt_client.is_connected():
            return

        wait_timeout_seconds = 2

        for lwt_topic in self.lwt_topics:
            msg_info: MQTTMessageInfo = self.mqtt_client.publish(
                lwt_topic, payload=self.PAYLOAD_LWT_OFFLINE, retain=False
            )
            msg_info.wait_for_publish(timeout=wait_timeout_seconds)
            self._logger.info("Published '%s' lwt message to MQTT topic '%s'", self.PAYLOAD_LWT_OFFLINE, lwt_topic)

    def pub_sensor_updates(self):
        """Publish updated sensor values to broker"""

        # update sensors value
        # update_sensors()

        # report our new sensor values to MQTT
        # _thread.start_new_thread(send_status, (current_timestamp, ''))
        self._logger.info("Published updated sensor data")
