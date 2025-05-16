"""Platform for light integration."""
from __future__ import annotations

import logging

import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import PLATFORM_SCHEMA
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up Generic BT device based on a config entry."""
    coordinator: GenericBTCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([GlowSwitch(coordinator)])

    platform = entity_platform.async_get_current_platform()

class GlowSwitch(LightEntity):
    """Representation of an Glowswitch Light (on/off only, assumed state)."""

    def __init__(self, light) -> None:
        self._light = light
        self._name = light.name
        self._state = False  # Start with off

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_on(self) -> bool | None:
        return self._state

    @property
    def assumed_state(self) -> bool:
        """Return True because we are assuming the state."""
        return True

    def turn_on(self, **kwargs) -> None:
        await self._device.write_gatt("12345678-1234-5678-1234-56789abcdef1", '01')
        self._state = True

    def turn_off(self, **kwargs) -> None:
        await self._device.write_gatt("12345678-1234-5678-1234-56789abcdef1", '00')
        self._state = False

    def update(self) -> None:
        """No polling, so skip fetching state."""
        pass
