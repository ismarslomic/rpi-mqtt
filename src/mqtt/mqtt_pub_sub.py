#!/usr/bin/env python3
"""Main module starting MQTT pub and sub"""

import logging
import os
import sys
from time import sleep

from mqtt.mqtt_client import RpiMqttClient
from mqtt.mqtt_pub import RpiMqttPublisher
from mqtt.repeat_timer import RepeatTimer
from mqtt.types import RpiMqttTopics
from sensors.main import create_sensors
from sensors.network.sensor import HostnameSensor
from sensors.types import AllRpiSensors, RpiSensor, SensorNotAvailableException
from settings.types import MqttSettings, ScriptSettings, SensorsMonitoringSettings, Settings


def _sensor_name(mqtt_settings: MqttSettings, logger: logging.Logger) -> str:
    sensor_name: str = mqtt_settings.sensor_name.lower()

    if sensor_name == "rpi-{hostname}":
        try:
            hostname_sensor = HostnameSensor(enabled=True)
            hostname_sensor.refresh_state()
            hostname = hostname_sensor.state

            sensor_name = f"rpi-{hostname}"
        except SensorNotAvailableException:
            logger.error(
                "Not possible to read hostname of this Rpi. Please set the 'mqtt.sensor_name' manually in settings.yml"
            )
            sys.exit(130)

    return sensor_name


def start_pub_sub(user_settings: Settings):
    """Function starting the MQTT pub and sub"""

    # Define logger
    logger: logging.Logger = logging.getLogger(__name__)

    # Settings
    mqtt_settings: MqttSettings = user_settings.mqtt
    script_settings: ScriptSettings = user_settings.script
    sensor_settings: SensorsMonitoringSettings = user_settings.sensors

    # Sensor name
    sensor_name: str = _sensor_name(mqtt_settings=mqtt_settings, logger=logger)

    # Mqtt Topics
    mqtt_topics = RpiMqttTopics(mqtt_settings=mqtt_settings, sensor_name=sensor_name)

    logger.info("Publish & Subscribe main script")

    lwt_update_interval_sec: int = 60
    sensor_update_interval_sec: int = script_settings.update_interval

    publisher: RpiMqttPublisher | None = None
    mqtt_client: RpiMqttClient | None = None
    lwt_update_scheduler: RepeatTimer | None = None
    sensor_update_scheduler: RepeatTimer | None = None

    # noinspection PyBroadException
    # pylint: disable=W0718
    try:
        # Mqtt client
        mqtt_client = RpiMqttClient(settings=mqtt_settings, mqtt_topics=mqtt_topics)
        mqtt_client.connect_and_loop()

        # Sensor states
        sensors: list[RpiSensor] = create_sensors(sensor_settings=sensor_settings)
        all_sensors: AllRpiSensors = AllRpiSensors(sensors=sensors, script_settings=script_settings)

        # Mqtt publisher
        publisher = RpiMqttPublisher(mqtt_client=mqtt_client, mqtt_topics=mqtt_topics, all_sensors=all_sensors)

        # Publish LWT messages initially and in repeat
        publisher.pub_online_lwt()
        lwt_update_scheduler = RepeatTimer(
            name="lwt_update_scheduler", interval=lwt_update_interval_sec, function=publisher.pub_online_lwt
        )
        lwt_update_scheduler.start()

        # Publish sensor data initially and in repeat
        publisher.pub_sensor_updates()
        sensor_update_scheduler = RepeatTimer(
            name="sensor_update_scheduler", interval=sensor_update_interval_sec, function=publisher.pub_sensor_updates
        )
        sensor_update_scheduler.start()

        while True:
            sleep(10000)
    except Exception:
        logger.error("Exception occurred", exc_info=True)
    finally:
        if publisher is not None:
            publisher.pub_offline_lwt()

        if lwt_update_scheduler is not None:
            lwt_update_scheduler.cancel()

        if sensor_update_scheduler is not None:
            sensor_update_scheduler.cancel()

        # Disconnect from MQTT and stop the background thread running loop()
        if mqtt_client is not None:
            mqtt_client.disconnect()
            logger.info("Disconnected from MQTT broker")

        try:
            logger.info("Exiting system with code 130")
            sys.exit(130)
        except SystemExit:
            logger.info("Exiting os with code 130")
            # noinspection PyUnresolvedReferences,PyProtectedMember
            os._exit(130)
