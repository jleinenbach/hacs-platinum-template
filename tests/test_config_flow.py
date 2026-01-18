"""Tests for config flow."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.your_domain.const import DOMAIN


async def test_user_flow_success(hass: HomeAssistant) -> None:
    """Test successful user flow."""
    with patch(
        "custom_components.your_domain.api.client.YourDomainApiClient"
    ) as mock_client:
        mock_client.return_value.async_validate_connection = AsyncMock(
            return_value=True
        )

        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.100"},
        )

        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == "192.168.1.100"
        assert result["data"] == {CONF_HOST: "192.168.1.100"}
