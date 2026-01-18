"""Config flow for Your Domain.

Bronze: config-flow - UI-based setup with data_description.
Bronze: test-before-configure - Validate connection in config flow.
Bronze: unique-config-entry - Prevent duplicate entries.
Silver: reauthentication-flow - UI-based reauth.
Gold: reconfiguration-flow - UI-based reconfiguration.
"""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_HOST
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .api.client import YourDomainApiClient
from .api.exceptions import (
    YourDomainApiAuthenticationError,
    YourDomainApiCommunicationError,
)
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): TextSelector(
            TextSelectorConfig(type=TextSelectorType.TEXT)
        ),
    }
)


class YourDomainConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Your Domain."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Bronze: unique-config-entry
            self._async_abort_entries_match({CONF_HOST: user_input[CONF_HOST]})

            # Bronze: test-before-configure
            session = async_get_clientsession(self.hass)
            client = YourDomainApiClient(
                host=user_input[CONF_HOST],
                session=session,
            )

            try:
                await client.async_validate_connection()
            except YourDomainApiAuthenticationError:
                errors["base"] = "invalid_auth"
            except YourDomainApiCommunicationError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_reauth(
        self,
        entry_data: dict[str, Any],
    ) -> ConfigFlowResult:
        """Handle reauthentication (Silver)."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle reauth confirmation."""
        errors: dict[str, str] = {}

        if user_input is not None:
            reauth_entry = self._get_reauth_entry()
            session = async_get_clientsession(self.hass)
            client = YourDomainApiClient(
                host=reauth_entry.data[CONF_HOST],
                session=session,
            )

            try:
                await client.async_validate_connection()
            except YourDomainApiAuthenticationError:
                errors["base"] = "invalid_auth"
            except YourDomainApiCommunicationError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_update_reload_and_abort(
                    reauth_entry,
                    data={**reauth_entry.data, **user_input},
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle reconfiguration (Gold)."""
        errors: dict[str, str] = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)
            client = YourDomainApiClient(
                host=user_input[CONF_HOST],
                session=session,
            )

            try:
                await client.async_validate_connection()
            except YourDomainApiAuthenticationError:
                errors["base"] = "invalid_auth"
            except YourDomainApiCommunicationError:
                errors["base"] = "cannot_connect"
            else:
                reconfigure_entry = self._get_reconfigure_entry()
                return self.async_update_reload_and_abort(
                    reconfigure_entry,
                    data={**reconfigure_entry.data, **user_input},
                )

        reconfigure_entry = self._get_reconfigure_entry()
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=reconfigure_entry.data.get(CONF_HOST),
                    ): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.TEXT)
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """Get the options flow."""
        return YourDomainOptionsFlow()


class YourDomainOptionsFlow(OptionsFlow):
    """Handle options flow."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )
