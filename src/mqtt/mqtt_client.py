#!/usr/bin/env python3
"""Subclass of the paho mqtt client"""

import logging
import os
import sys
from time import sleep

import paho.mqtt.client as mqtt

from mqtt.mqtt_pub import RpiMqttPublisher
from settings.types import MqttSettings


class RpiMqttClient(mqtt.Client):
    """Subclass of the paho mqtt client"""

    settings: MqttSettings
    _rpi_mqtt_logger: logging.Logger
    command_topic_names: list[str] = []
    command_base_topic: str

    def __init__(self, settings: MqttSettings, lwt_topic_names: list[str], command_base_topic: str):
        super().__init__(client_id=settings.client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

        self.on_connect = self.on_connect_callback
        self.on_message = self.on_message_callback
        self.on_disconnect = self.on_disconnect_callback
        self.on_connect_fail = self.on_connect_fail_callback

        self.settings = settings
        self._rpi_mqtt_logger = logging.getLogger(__name__)
        self.enable_logger()
        self.lwt_topic_names = lwt_topic_names
        self.command_base_topic = command_base_topic

    def connect_and_loop(self):
        """Connect to the broker and use loop_start() to set a thread running to call loop()"""

        # Define will message for lwt topics
        for lwt_topic in self.lwt_topic_names:
            self.will_set(lwt_topic, payload=RpiMqttPublisher.PAYLOAD_LWT_OFFLINE, retain=True)

        # noinspection PyBroadException
        # pylint: disable=W0718
        try:
            self.connect(host=self.settings.hostname, port=self.settings.port, keepalive=60)

            # Runs a thread in the background to call loop() automatically
            self.loop_start()

            while not self.is_connected():  # wait for mqtt connection in loop, 1 sec sleep
                self._rpi_mqtt_logger.debug("Wait on MQTT connection")
                sleep(1.0)
        except Exception:
            self._rpi_mqtt_logger.error("Failed connecting to MQTT broker", exc_info=True)
            sys.exit(1)

    # noinspection PyMethodOverriding
    # pylint: disable=W0613, R0913
    def on_connect_callback(self, client: mqtt.Client, userdata, flags, reason_code: mqtt.ReasonCode, properties):
        """The callback called when the broker responds to our connection request."""

        if reason_code.is_failure:
            self._rpi_mqtt_logger.error("Failed to connect: '%s'. loop() will retry connection", reason_code)

            # kill main thread
            # noinspection PyUnresolvedReferences,PyProtectedMember
            os._exit(1)
        else:
            # we should always subscribe from on_connect callback to be sure
            # our subscribed is persisted across reconnections.

            # Commands Subscription
            command_topics: list[str] = self.command_topic_names
            if len(command_topics) > 0:
                for command_topic in command_topics:
                    self._rpi_mqtt_logger.info("Subscribing to command topic '%s'", command_topic)
                    client.subscribe(f"{command_topic}/+")
            else:
                self._rpi_mqtt_logger.debug("None command topics to subscribe to")

            self._rpi_mqtt_logger.info(
                "Connected to MQTT broker '%s:%d' with result code '%s'",
                self.settings.hostname,
                self.settings.port,
                reason_code,
            )
            # client.subscribe("$SYS/#")

    # noinspection PyMethodOverriding
    # pylint: disable=W0613
    def on_message_callback(self, client, userdata, msg: mqtt.MQTTMessage):
        """The callback called when a message has been received on a topic that the client subscribes to."""

        self._rpi_mqtt_logger.debug("Reading new message from MQTT.")
        print(msg.topic + " " + str(msg.payload))

    # noinspection PyMethodOverriding
    # pylint: disable=W0613, R0913
    def on_disconnect_callback(self, client, userdata, disconnect_flags, reason_code, properties):
        """The callback called when the client disconnects from the broker."""

        self._rpi_mqtt_logger.warning("Connection lost to the MQTT broker. Reconnecting.")

    # noinspection PyMethodOverriding
    # pylint: disable=W0613
    def on_connect_fail_callback(self, client, userdata):
        """The callback called when the client failed to connect to the broker."""

        self._rpi_mqtt_logger.warning("Failed connecting to the MQTT broker.")
