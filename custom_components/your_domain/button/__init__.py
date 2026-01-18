"""Button platform for Your Domain."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription

from ..entity import YourDomainEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .. import YourDomainConfigEntry

BUTTONS: tuple[ButtonEntityDescription, ...] = (
    ButtonEntityDescription(
        key="restart",
        translation_key="restart",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: YourDomainConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up button platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        YourDomainButton(coordinator, description)
        for description in BUTTONS
    )


class YourDomainButton(YourDomainEntity, ButtonEntity):
    """Button entity for Your Domain."""

    async def async_press(self) -> None:
        """Handle button press."""
        await self.coordinator.async_request_refresh()
