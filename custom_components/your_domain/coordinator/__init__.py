"""DataUpdateCoordinator for Your Domain.

Silver: log-when-unavailable - Log once on disconnect/reconnect.
"""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api.exceptions import (
    YourDomainApiAuthenticationError,
    YourDomainApiCommunicationError,
)
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from .api.client import YourDomainApiClient

_LOGGER = logging.getLogger(__name__)


class YourDomainCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for Your Domain.

    Silver: log-when-unavailable - Uses _unavailable_logged flag.
    """

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: YourDomainApiClient,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.client = client
        self.config_entry = entry

        # Silver: log-when-unavailable - Track if we logged unavailable
        self._unavailable_logged: bool = False

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the API.

        Silver: log-when-unavailable - Log once on state changes.
        """
        try:
            data = await self.client.async_get_data()

            # Silver: log-when-unavailable - Log ONCE when restored
            if self._unavailable_logged:
                _LOGGER.info(
                    "Connection to %s restored",
                    self.client.host,
                )
                self._unavailable_logged = False

            return data

        except YourDomainApiAuthenticationError as err:
            # Trigger reauth flow
            self.config_entry.async_start_reauth(self.hass)
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="auth_failed",
            ) from err

        except YourDomainApiCommunicationError as err:
            # Silver: log-when-unavailable - Log ONCE when unavailable
            if not self._unavailable_logged:
                _LOGGER.warning(
                    "Unable to connect to %s: %s",
                    self.client.host,
                    err,
                )
                self._unavailable_logged = True

            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="cannot_connect",
            ) from err
