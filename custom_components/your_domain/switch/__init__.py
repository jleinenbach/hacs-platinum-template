"""Switch platform for Your Domain."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from ..entity import YourDomainEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .. import YourDomainConfigEntry

SWITCHES: tuple[SwitchEntityDescription, ...] = (
    SwitchEntityDescription(
        key="example_switch",
        translation_key="example_switch",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: YourDomainConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        YourDomainSwitch(coordinator, description)
        for description in SWITCHES
    )


class YourDomainSwitch(YourDomainEntity, SwitchEntity):
    """Switch entity for Your Domain."""

    _attr_is_on: bool = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        self._attr_is_on = False
        self.async_write_ha_state()
