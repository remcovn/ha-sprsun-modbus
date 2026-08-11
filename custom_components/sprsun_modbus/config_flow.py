"""Config flow for SPRSUN Modbus."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_PROFILE,
    DEFAULT_PORT,
    DEFAULT_PROFILE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SLAVE,
    DOMAIN,
    PROFILE_OPTIONS,
)

CONF_SLAVE = "slave"


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535)),
        vol.Required(CONF_SLAVE, default=DEFAULT_SLAVE): vol.All(vol.Coerce(int), vol.Range(min=1, max=247)),
        vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int),
            vol.Range(min=5, max=3600),
        ),
        vol.Required(CONF_PROFILE, default=DEFAULT_PROFILE): vol.In(PROFILE_OPTIONS),
    }
)


class SprsunModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SPRSUN Modbus."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> "SprsunModbusOptionsFlow":
        """Return the options flow for this handler."""
        return SprsunModbusOptionsFlow(config_entry)

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

        host = user_input[CONF_HOST]
        port = user_input[CONF_PORT]
        slave = user_input[CONF_SLAVE]

        await self.async_set_unique_id(f"{host}:{port}:{slave}")
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=f"SPRSUN {host}:{port} (slave {slave})", data=user_input)


class SprsunModbusOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for SPRSUN Modbus."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Manage the integration options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_scan = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        current_host = self.config_entry.options.get(CONF_HOST, self.config_entry.data.get(CONF_HOST, ""))
        current_port = self.config_entry.options.get(CONF_PORT, self.config_entry.data.get(CONF_PORT, DEFAULT_PORT))
        current_slave = self.config_entry.options.get(CONF_SLAVE, self.config_entry.data.get(CONF_SLAVE, DEFAULT_SLAVE))
        current_profile = self.config_entry.options.get(
            CONF_PROFILE,
            self.config_entry.data.get(CONF_PROFILE, DEFAULT_PROFILE),
        )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=current_host): str,
                vol.Required(CONF_PORT, default=current_port): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535)),
                vol.Required(CONF_SLAVE, default=current_slave): vol.All(vol.Coerce(int), vol.Range(min=1, max=247)),
                vol.Required(CONF_SCAN_INTERVAL, default=current_scan): vol.All(
                    vol.Coerce(int),
                    vol.Range(min=5, max=3600),
                ),
                vol.Required(CONF_PROFILE, default=current_profile): vol.In(PROFILE_OPTIONS),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)

