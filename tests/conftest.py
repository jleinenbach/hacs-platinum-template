"""Test fixtures for Your Domain."""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.const import CONF_HOST
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.your_domain.const import DOMAIN


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations: None,
) -> Generator[None, None, None]:
    """Enable custom integrations."""
    yield


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Create mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "192.168.1.100"},
        entry_id="test_entry_id",
        title="Test Device",
    )


@pytest.fixture
def mock_api_client() -> Generator[AsyncMock, None, None]:
    """Create mock API client."""
    with patch(
        "custom_components.your_domain.api.client.YourDomainApiClient"
    ) as mock:
        client = mock.return_value
        client.host = "192.168.1.100"
        client.async_validate_connection = AsyncMock(return_value=True)
        client.async_get_data = AsyncMock(return_value={"value": 42})
        yield client
