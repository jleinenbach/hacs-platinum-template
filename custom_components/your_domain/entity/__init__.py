"""Base entity for Your Domain.

Bronze: has-entity-name - All entities have has_entity_name = True.
Bronze: entity-unique-id - All entities have unique IDs.
Gold: devices - Creates devices via DeviceInfo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

if TYPE_CHECKING:
    from .coordinator import YourDomainCoordinator


class YourDomainEntity(CoordinatorEntity["YourDomainCoordinator"]):
    """Base entity for Your Domain.

    Bronze: has-entity-name - _attr_has_entity_name = True
    Bronze: entity-unique-id - Unique ID from entry_id + key
    Gold: devices - DeviceInfo with identifiers
    """

    _attr_has_entity_name = True  # Bronze: REQUIRED

    def __init__(
        self,
        coordinator: YourDomainCoordinator,
        description: EntityDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = description

        # Bronze: entity-unique-id
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{description.key}"
        )

        # Gold: devices - Create device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name=coordinator.config_entry.title,
            manufacturer="Your Manufacturer",
            model="Your Model",
            sw_version="1.0.0",
        )
