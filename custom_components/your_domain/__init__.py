"""Your Domain Integration for Home Assistant.

This integration targets Platinum Quality Scale standards.
See quality_scale.yaml for compliance tracking.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.const import CONF_HOST, Platform
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api.client import YourDomainApiClient
from .api.exceptions import (
    YourDomainApiAuthenticationError,
    YourDomainApiCommunicationError,
)
from .const import DOMAIN
from .coordinator import YourDomainCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

# Platforms to set up
PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.BUTTON,
]

# Type alias for config entry (Platinum: strict-typing)
type YourDomainConfigEntry = ConfigEntry[YourDomainData]


@dataclass
class YourDomainData:
    """Runtime data for the integration (Bronze: runtime-data)."""

    coordinator: YourDomainCoordinator
    client: YourDomainApiClient


async def async_setup_entry(
    hass: HomeAssistant,
    entry: YourDomainConfigEntry,
) -> bool:
    """Set up Your Domain from a config entry.

    Bronze: test-before-setup - Check connectivity before setup.
    Platinum: inject-websession - Pass session to client.
    """
    # Platinum: inject-websession - Get session from Home Assistant
    session = async_get_clientsession(hass)

    client = YourDomainApiClient(
        host=entry.data[CONF_HOST],
        session=session,
    )

    # Bronze: test-before-setup - Validate connection
    try:
        await client.async_validate_connection()
    except YourDomainApiAuthenticationError as err:
        raise ConfigEntryAuthFailed(
            translation_domain=DOMAIN,
            translation_key="auth_failed",
        ) from err
    except YourDomainApiCommunicationError as err:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="cannot_connect",
        ) from err

    # Create coordinator
    coordinator = YourDomainCoordinator(hass, client, entry)

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Bronze: runtime-data - Store in runtime_data, NOT hass.data
    entry.runtime_data = YourDomainData(
        coordinator=coordinator,
        client=client,
    )

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: YourDomainConfigEntry,
) -> bool:
    """Unload a config entry.

    Silver: config-entry-unloading - Support unloading.
    """
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
