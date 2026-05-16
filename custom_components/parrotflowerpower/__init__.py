"""Parrot Flower Power BLE plant sensor integration."""
from __future__ import annotations

import logging

from bleak import BleakClient
from bleak.exc import BleakError
from bleak_retry_connector import establish_connection

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    DEFAULT_POLL_INTERVAL,
    UUID_BATTERY,
    UUID_LIGHT,
    UUID_SOIL_CONDUCTIVITY,
    UUID_SOIL_TEMPERATURE,
    UUID_AIR_TEMPERATURE,
    UUID_SOIL_MOISTURE,
    UUID_CALIBRATED_MOISTURE,
)
from .parser import (
    parse_raw_uint16,
    calibrate_light,
    calibrate_temperature,
    calibrate_moisture,
    calibrate_conductivity,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Parrot Flower Power from a config entry."""
    address: str = entry.data["address"]

    coordinator = ParrotFlowerPowerCoordinator(hass, address)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


class ParrotFlowerPowerCoordinator(DataUpdateCoordinator):
    """Coordinator that polls Parrot Flower Power via GATT."""

    def __init__(self, hass: HomeAssistant, address: str) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"Parrot Flower Power {address}",
            update_interval=DEFAULT_POLL_INTERVAL,
        )
        self.address = address

    async def _async_update_data(self) -> dict[str, float | None]:
        """Connect to device, read all sensors, return parsed data."""
        ble_device = bluetooth.async_ble_device_from_address(
            self.hass, self.address, connectable=True
        )
        if not ble_device:
            raise UpdateFailed(f"Device {self.address} not available")

        data: dict[str, float | None] = {}

        try:
            client = await establish_connection(
                BleakClient, ble_device, self.address
            )
            try:
                # Battery (uint8)
                raw = await client.read_gatt_char(UUID_BATTERY)
                data["battery"] = float(raw[0])

                # Light (uint16 LE)
                raw = await client.read_gatt_char(UUID_LIGHT)
                data["light"] = calibrate_light(parse_raw_uint16(raw))

                # Soil Conductivity (uint16 LE)
                raw = await client.read_gatt_char(UUID_SOIL_CONDUCTIVITY)
                data["conductivity"] = calibrate_conductivity(parse_raw_uint16(raw))

                # Soil Temperature (uint16 LE)
                raw = await client.read_gatt_char(UUID_SOIL_TEMPERATURE)
                data["soil_temperature"] = calibrate_temperature(parse_raw_uint16(raw))

                # Air Temperature (uint16 LE)
                raw = await client.read_gatt_char(UUID_AIR_TEMPERATURE)
                data["air_temperature"] = calibrate_temperature(parse_raw_uint16(raw))

                # Soil Moisture (uint16 LE)
                raw = await client.read_gatt_char(UUID_SOIL_MOISTURE)
                data["moisture"] = calibrate_moisture(parse_raw_uint16(raw))

                # Calibrated Moisture (firmware 1.1.0+, may not exist)
                try:
                    raw = await client.read_gatt_char(UUID_CALIBRATED_MOISTURE)
                    if len(raw) == 4:
                        import struct
                        data["moisture_cal"] = round(struct.unpack("<f", raw)[0], 1)
                    else:
                        data["moisture_cal"] = None
                except (BleakError, Exception):
                    data["moisture_cal"] = None

            finally:
                await client.disconnect()

        except BleakError as err:
            raise UpdateFailed(f"BLE connection failed: {err}") from err
        except TimeoutError as err:
            raise UpdateFailed(f"BLE connection timed out: {err}") from err

        _LOGGER.debug("Polled %s: %s", self.address, data)
        return data
