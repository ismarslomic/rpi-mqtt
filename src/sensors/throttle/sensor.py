#!/usr/bin/env python3
"""Service for reading the system thermal throttling of Rpi"""

import subprocess
from typing import Union

from sensors.throttle.types import SystemThrottleStatus
from sensors.types import RpiSensor, SensorNotAvailableException


class ThrottledSensor(RpiSensor):
    """Sensor for thermal throttling"""

    _state: SystemThrottleStatus | None = None

    @property
    def name(self) -> str:
        return "throttled"

    @property
    def state(self) -> SystemThrottleStatus | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_throttle_status()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_throttle_status(self) -> SystemThrottleStatus:
        """Read current system thermal throttled status"""

        # doc: https://www.raspberrypi.com/documentation/computers/os.html#get_throttled

        args = ["vcgencmd", "get_throttled"]
        try:
            result = subprocess.run(args, capture_output=True, text=True, check=False)
        except FileNotFoundError as err2:
            self.logger.warning("vcgencmd not available for this Rpi")
            raise SensorNotAvailableException("vcgencmd not available for this Rpi") from err2

        if result.returncode != 0:
            self.logger.warning(
                "Process 'vcgencmd get_throttled' returned code %s: %s", str(result.returncode), str(result.stderr)
            )
            raise SensorNotAvailableException("Failed to read throttled state", result.stderr)

        # result.stdout: throttled=0x0
        throttle_status_raw: str = result.stdout.strip()

        status_hex: str | None = self._get_status_as_hex(throttle_status_raw)

        if status_hex is None:
            raise SensorNotAvailableException(f"Bad response from vcgencmd get_throttled: '{throttle_status_raw}'")

        status_decimal: int = self._convert_hex_to_integer(status_hex)
        status_binary: str = bin(status_decimal)
        throttled_reasons: str = self._to_human_readable(status_decimal)

        return SystemThrottleStatus(
            status_hex=status_hex, status_decimal=status_decimal, status_binary=status_binary, reason=throttled_reasons
        )

    def _get_status_as_hex(self, raw: str) -> Union[str, None]:
        """Returns the throttled value from string, example raw='throttled=0x0', returns '0x0'. Returns None if raw is
        not in this format"""

        raw_list: list[str] = raw.split("=")

        if len(raw_list) > 1:
            return raw_list[1]

        self.logger.warning("List size is not >1, size=%d", len(raw_list))
        return None

    @staticmethod
    def _convert_hex_to_integer(hex_value: str) -> int:
        """Returns hex string as integer, example hex_value: '0x50000', returns 327680"""

        # Set the base to 0 to let Python figure it out based on the 0x
        return int(hex_value, 0)

    @staticmethod
    def _to_human_readable(throttled_value: int) -> str:
        """Translates the throttled status expressed as integer to human-readable status"""

        # doc: https://blog.mccormack.tech/shell/2019/01/05/monitoring-raspberry-pi-power-and-thermal-issues.html
        # doc: https://www.raspberrypi.com/documentation/computers/os.html#get_throttled
        # doc: https://chem.libretexts.org/Courses/Intercollegiate_Courses/
        # Internet_of_Science_Things/5%3A_Appendix_3%3A_General_Tasks/5.9%3A_Monitoring_your_Raspberry_Pi

        # Example: when we convert int value to binary value, we can see that bit 1, 16, 17 and 18 is set (1 means on)
        # 01110000000000000010
        # ||||            ||||_ 0: Under-voltage detected
        # ||||            |||_ 1: Arm frequency capped
        # ||||            ||_ 2: Currently throttled
        # ||||            |_ 3: Soft temperature limit active
        # ||||_ 16: Under-voltage has occurred
        # |||_ 17: Arm frequency capped has occurred
        # ||_ 18: Throttling has occurred
        # |_ 19: Soft temperature limit has occurred

        bits_and_reasons = [
            (2**0, "Under-voltage detected"),
            (2**1, "Arm frequency capped"),
            (2**2, "Currently throttled"),
            (2**3, "Soft temperature limit active"),
            (2**16, "Under-voltage has occurred"),
            (2**17, "Arm frequency capped has occurred"),
            (2**18, "Throttling has occurred"),
            (2**19, "Soft temperature limit has occurred"),
        ]

        throttled_reasons: list[str] = []

        for _, bit_and_reason in enumerate(bits_and_reasons):
            bit = bit_and_reason[0]
            reason = bit_and_reason[1]

            # & is bitwise AND operator, see https://realpython.com/python-operators-expressions/
            if throttled_value & bit > 0:
                throttled_reasons.append(reason)

        if len(throttled_reasons) == 0:
            return "Not throttled"

        # Example: 'Under-voltage has occurred. Throttling has occurred'
        return ". ".join(throttled_reasons)
