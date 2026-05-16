"""Sensor platform for Parrot Flower Power."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfIlluminance, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="air_temperature",
        translation_key="air_temperature",
        name="Air Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="soil_temperature",
        translation_key="soil_temperature",
        name="Soil Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="light",
        translation_key="light",
        name="Light Intensity",
        native_unit_of_measurement=UnitOfIlluminance.LUX,
        device_class=SensorDeviceClass.ILLUMINANCE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="moisture",
        translation_key="moisture",
        name="Soil Moisture",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water-percent",
    ),
    SensorEntityDescription(
        key="moisture_cal",
        translation_key="moisture_cal",
        name="Calibrated Moisture",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water-percent",
    ),
    SensorEntityDescription(
        key="conductivity",
        translation_key="conductivity",
        name="Soil Conductivity",
        native_unit_of_measurement="µS/cm",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash-circle",
    ),
    SensorEntityDescription(
        key="battery",
        translation_key="battery",
        name="Battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Parrot Flower Power sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    address = entry.data["address"]

    entities = [
        ParrotFlowerPowerSensor(coordinator, description, address, entry)
        for description in SENSOR_DESCRIPTIONS
    ]
    async_add_entities(entities)


class ParrotFlowerPowerSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Parrot Flower Power sensor."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, description: SensorEntityDescription, address: str, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{address}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, address)},
            name=entry.title,
            manufacturer="Parrot",
            model="Flower Power",
        )

    @property
    def native_value(self) -> float | None:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def available(self) -> bool:
        """Return True if coordinator has data."""
        return super().available and self.coordinator.data is not None
