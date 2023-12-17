#!/usr/bin/env python3
"""Main module starting MQTT pub and sub"""

from mqtt.pub.mqtt_pub import publish
from mqtt.sub.mqtt_sub import subscribe


def main():
    """Function starting the MQTT pub and sub"""

    print("Publish & Subscribe main script")
    publish()
    subscribe()


if __name__ == "__main__":
    main()
