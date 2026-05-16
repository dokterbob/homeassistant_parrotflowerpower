"""Calibration and parsing functions for Parrot FlowerPower BLE sensor data."""


def parse_raw_uint16(data: bytes) -> int:
    """Parse a 2-byte little-endian unsigned integer."""
    return int.from_bytes(data[:2], byteorder="little", signed=False)


def calibrate_light(raw_value: int) -> float:
    """Calibrate raw light sensor value to lux (WatchFlower formula).

    Returns 0.0 for invalid readings (0 or 65535).
    """
    if raw_value == 0 or raw_value == 65535:
        return 0.0
    lux = 1000.0 * 0.08640000000000001 * (192773.17000000001 * raw_value ** (-1.0606619))
    return round(lux, 1)


def calibrate_temperature(raw_value: int) -> float:
    """Calibrate raw temperature sensor value to degrees Celsius.

    Result is clamped to [-10, 55].
    """
    temp = (
        0.00000003044 * raw_value ** 3
        - 0.00008038 * raw_value ** 2
        + 0.1149 * raw_value
        - 30.45
    )
    temp = max(-10.0, min(55.0, temp))
    return round(temp, 1)


def calibrate_moisture(raw_value: int) -> float:
    """Calibrate raw soil moisture sensor value to percentage.

    Two-step polynomial calibration. Result is clamped to [0, 60].
    """
    # Step 1: raw to hygro
    hygro = 11.4293 + (
        0.0000000010698 * raw_value ** 4
        - 0.00000152538 * raw_value ** 3
        + 0.000866976 * raw_value ** 2
        - 0.169422 * raw_value
    )
    # Step 2: hygro to percentage
    pct = 100.0 * (
        0.0000045 * hygro ** 3
        - 0.00055 * hygro ** 2
        + 0.0292 * hygro
        - 0.053
    )
    pct = max(0.0, min(60.0, pct))
    return round(pct, 1)


def calibrate_conductivity(raw_value: int) -> float:
    """Calibrate raw soil conductivity sensor value."""
    return round(raw_value / 1.771, 1)
