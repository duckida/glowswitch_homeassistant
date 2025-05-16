from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers import entity_platform
from homeassistant.components.light import PLATFORM_SCHEMA, LightEntity

# Removed DEFAULT_CHAR_UUID import per user request.
from .const import DOMAIN
from .coordinator import GenericBTCoordinator
from .entity import GenericBTEntity

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required("address"): cv.string,
})

# Hardcoded GATT characteristic UUID for GlowSwitch control
GLOWSWITCH_CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the GlowSwitch platform from YAML configuration."""
    address = config["address"]
    # Initialize or retrieve coordinator for this device
    coordinator = hass.data.setdefault(DOMAIN, {}).get(address)
    if not coordinator:
        coordinator = GenericBTCoordinator(hass, address)
        hass.data[DOMAIN][address] = coordinator
        await coordinator.async_config_entry_first_refresh()

    async_add_entities([GlowSwitch(coordinator)], True)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the GlowSwitch platform from a config entry."""
    coordinator: GenericBTCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([GlowSwitch(coordinator)], True)

class GlowSwitch(GenericBTEntity, LightEntity):
    """Representation of a GlowSwitch Light (on/off only, assumed state)."""

    def __init__(self, coordinator: GenericBTCoordinator) -> None:
        """Initialize the light."""
        super().__init__(coordinator)
        self._attr_name = coordinator.device_name
        self._attr_unique_id = f"{coordinator.address}-glow-switch"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.address)},
            "name": coordinator.device_name,
            "manufacturer": coordinator.manufacturer,
            "model": coordinator.model,
        }
        self._state = False

    @property
    def is_on(self) -> bool:
        return self._state

    @property
    def assumed_state(self) -> bool:
        """Return True because we are assuming the state."""
        return True

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        await self.coordinator.client.char_write(
            GLOWSWITCH_CHAR_UUID, b"\x01"
        )
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        await self.coordinator.client.char_write(
            GLOWSWITCH_CHAR_UUID, b"\x00"
        )
        self._state = False
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """No polling needed; state is assumed."""
        return
