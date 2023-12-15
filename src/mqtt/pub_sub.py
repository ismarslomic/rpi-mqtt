#!/usr/bin/env python3
from mqtt.pub.mqtt_pub import publish
from mqtt.sub.mqtt_sub import subscribe


def main():
    print("Publish & Subscribe main script")
    publish()
    subscribe()


if __name__ == "__main__":
    main()
