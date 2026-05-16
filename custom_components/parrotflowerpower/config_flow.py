"""Config flow for Parrot Flower Power."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.device_registry import format_mac

from .const import DOMAIN, DEVICE_MAC_PREFIXES

MANUAL_MAC = "manual"


class ParrotFlowerPowerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Parrot Flower Power."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, BluetoothServiceInfoBleak] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> ConfigFlowResult:
        """Handle Bluetooth discovery."""
        await self.async_set_unique_id(format_mac(discovery_info.address))
        self._abort_if_unique_id_configured()
        self._discovery_info = discovery_info
        self.context["title_placeholders"] = {
            "name": discovery_info.name or "Flower Power"
        }
        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm Bluetooth discovery."""
        assert self._discovery_info is not None
        if user_input is not None:
            return self.async_create_entry(
                title=self._discovery_info.name or "Flower Power",
                data={"address": self._discovery_info.address},
            )
        self._set_confirm_only()
        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders={
                "name": self._discovery_info.name or "Flower Power"
            },
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the user step."""
        if user_input is not None:
            if user_input["address"] == MANUAL_MAC:
                return await self.async_step_manual()

            address = user_input["address"]
            await self.async_set_unique_id(
                format_mac(address), raise_on_progress=False
            )
            self._abort_if_unique_id_configured()

            service_info = self._discovered_devices.get(address)
            name = service_info.name if service_info else "Flower Power"
            return self.async_create_entry(
                title=name,
                data={"address": address},
            )

        already_configured = self._async_current_ids(False)
        devices: dict[str, str] = {}
        for service_info in async_discovered_service_info(self.hass, connectable=True):
            if (
                service_info.address.upper().startswith(DEVICE_MAC_PREFIXES)
                and format_mac(service_info.address) not in already_configured
            ):
                devices[service_info.address] = (
                    f"{service_info.name} ({service_info.address})"
                )
                self._discovered_devices[service_info.address] = service_info

        if not devices:
            return await self.async_step_manual()

        devices[MANUAL_MAC] = "Enter MAC address manually"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required("address"): vol.In(devices)}
            ),
        )

    async def async_step_manual(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle manual MAC entry."""
        if user_input is not None:
            address = user_input["address"].upper()
            await self.async_set_unique_id(
                format_mac(address), raise_on_progress=False
            )
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"Flower Power ({address})",
                data={"address": address},
            )

        return self.async_show_form(
            step_id="manual",
            data_schema=vol.Schema(
                {vol.Required("address"): str}
            ),
        )
