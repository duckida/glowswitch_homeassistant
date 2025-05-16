"""Platform for light integration."""
from __future__ import annotations

import logging

import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (ATTR_BRIGHTNESS, PLATFORM_SCHEMA,
                                            LightEntity)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)


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
        self._light.turn_on()
        self._state = True

    def turn_off(self, **kwargs) -> None:
        self._light.turn_off()
        self._state = False

    def update(self) -> None:
        """No polling, so skip fetching state."""
        pass
