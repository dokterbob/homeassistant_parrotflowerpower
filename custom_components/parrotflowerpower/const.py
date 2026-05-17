"""Constants for the Parrot FlowerPower BLE integration."""

import logging
from datetime import timedelta

DOMAIN = "parrotflowerpower"
LOGGER = logging.getLogger("custom_components.parrotflowerpower")

# Default polling interval
DEFAULT_POLL_INTERVAL = timedelta(minutes=15)

# Maximum random jitter (seconds) added to poll interval to stagger device reads
DEFAULT_POLL_JITTER_SECONDS = 60

# Consecutive poll failures before sensors are marked unavailable
DEFAULT_MAX_POLL_FAILURES = 4

# GATT characteristic UUIDs
UUID_BATTERY = "00002a19-0000-1000-8000-00805f9b34fb"
UUID_LIVE_SERVICE = "39e1fa00-84a8-11e2-afba-0002a5d5c51b"
UUID_LIGHT = "39e1fa01-84a8-11e2-afba-0002a5d5c51b"
UUID_SOIL_CONDUCTIVITY = "39e1fa02-84a8-11e2-afba-0002a5d5c51b"
UUID_SOIL_TEMPERATURE = "39e1fa03-84a8-11e2-afba-0002a5d5c51b"
UUID_AIR_TEMPERATURE = "39e1fa04-84a8-11e2-afba-0002a5d5c51b"
UUID_SOIL_MOISTURE = "39e1fa05-84a8-11e2-afba-0002a5d5c51b"
UUID_CALIBRATED_MOISTURE = "39e1fa09-84a8-11e2-afba-0002a5d5c51b"  # fw 1.1.0+ only

# Known Parrot FlowerPower MAC address prefixes
DEVICE_MAC_PREFIXES = ("A0:14:3D", "90:03:B7")

# Config entry keys
CONF_ADDRESS = "address"
