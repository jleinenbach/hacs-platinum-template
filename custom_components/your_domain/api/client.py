"""API Client for Your Domain.

Platinum requirements:
- async-dependency: All operations are async
- inject-websession: Session is injected, not created
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from .exceptions import (
    YourDomainApiAuthenticationError,
    YourDomainApiCommunicationError,
    YourDomainApiError,
)

if TYPE_CHECKING:
    from aiohttp import ClientSession


class YourDomainApiClient:
    """API client for Your Domain.

    Platinum: inject-websession - Session is injected from Home Assistant.
    Platinum: async-dependency - All methods are async.
    """

    def __init__(
        self,
        host: str,
        session: ClientSession,
        timeout: int = 10,
    ) -> None:
        """Initialize the API client.

        Args:
            host: The host address of the device.
            session: aiohttp ClientSession (injected from HA).
            timeout: Request timeout in seconds.

        """
        self._host = host
        self._session = session  # Platinum: inject-websession
        self._timeout = timeout

    @property
    def host(self) -> str:
        """Return the host address."""
        return self._host

    async def async_validate_connection(self) -> bool:
        """Validate the connection to the device.

        Returns:
            True if connection is valid.

        Raises:
            YourDomainApiAuthenticationError: Invalid credentials.
            YourDomainApiCommunicationError: Cannot connect.

        """
        return await self._async_request("GET", "/api/status")

    async def async_get_data(self) -> dict[str, Any]:
        """Get device data.

        Returns:
            Device data dictionary.

        Raises:
            YourDomainApiError: On any API error.

        """
        return await self._async_request("GET", "/api/data")

    async def _async_request(
        self,
        method: str,
        path: str,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Make an async request.

        Platinum: async-dependency - Uses asyncio.timeout (NOT async_timeout).

        Args:
            method: HTTP method.
            path: API path.
            data: Optional request data.

        Returns:
            Response data.

        Raises:
            YourDomainApiAuthenticationError: On auth errors (401/403).
            YourDomainApiCommunicationError: On connection errors.
            YourDomainApiError: On other errors.

        """
        url = f"http://{self._host}{path}"

        try:
            # CRITICAL: Use asyncio.timeout, NOT async_timeout
            async with asyncio.timeout(self._timeout):
                async with self._session.request(
                    method,
                    url,
                    json=data,
                ) as response:
                    if response.status in (401, 403):
                        raise YourDomainApiAuthenticationError(
                            f"Authentication failed: {response.status}"
                        )

                    if response.status >= 400:
                        raise YourDomainApiError(
                            f"API error: {response.status}"
                        )

                    return await response.json()

        except TimeoutError as err:
            raise YourDomainApiCommunicationError(
                f"Timeout connecting to {self._host}"
            ) from err
        except YourDomainApiError:
            raise
        except Exception as err:
            raise YourDomainApiCommunicationError(
                f"Error communicating with {self._host}: {err}"
            ) from err
