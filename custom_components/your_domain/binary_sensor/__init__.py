"""Binary sensor platform for Your Domain."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from ..entity import YourDomainEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .. import YourDomainConfigEntry

BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="connectivity",
        translation_key="connectivity",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: YourDomainConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensor platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        YourDomainBinarySensor(coordinator, description)
        for description in BINARY_SENSORS
    )


class YourDomainBinarySensor(YourDomainEntity, BinarySensorEntity):
    """Binary sensor entity for Your Domain."""

    @property
    def is_on(self) -> bool:
        """Return true if connected."""
        return self.coordinator.last_update_success
