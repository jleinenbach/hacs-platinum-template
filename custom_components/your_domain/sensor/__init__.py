"""Sensor platform for Your Domain."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

from ..entity import YourDomainEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .. import YourDomainConfigEntry

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="example_sensor",
        translation_key="example_sensor",
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: YourDomainConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        YourDomainSensor(coordinator, description)
        for description in SENSORS
    )


class YourDomainSensor(YourDomainEntity, SensorEntity):
    """Sensor entity for Your Domain."""

    @property
    def native_value(self) -> float | None:
        """Return the sensor value."""
        return self.coordinator.data.get("value")
