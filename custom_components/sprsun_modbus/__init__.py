"""The SPRSUN Modbus integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
    CONF_HOST,
    CONF_PORT,
    CONF_PROFILE,
    CONF_SCAN_INTERVAL,
    CONF_SLAVE,
    DATA_API,
    DATA_COORDINATOR,
    DEFAULT_PORT,
    DEFAULT_PROFILE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SLAVE,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import SprsunDataCoordinator
from .modbus_api import SprsunModbusApi
from .register_definitions import SENSOR_REGISTERS, WRITABLE_NUMBER_REGISTERS


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload entry after options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SPRSUN Modbus from a config entry."""
    host = entry.options.get(CONF_HOST, entry.data.get(CONF_HOST))
    port = entry.options.get(CONF_PORT, entry.data.get(CONF_PORT, DEFAULT_PORT))
    slave = entry.options.get(CONF_SLAVE, entry.data.get(CONF_SLAVE, DEFAULT_SLAVE))
    scan_interval = entry.options.get(
        CONF_SCAN_INTERVAL,
        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    )
    profile = entry.options.get(CONF_PROFILE, entry.data.get(CONF_PROFILE, DEFAULT_PROFILE))

    if not host:
        raise ConfigEntryNotReady("Host is missing in config entry")

    api = SprsunModbusApi(host=host, port=int(port), slave=int(slave))

    all_addresses = [definition.address for definition in SENSOR_REGISTERS]
    all_addresses.extend(definition.address for definition in WRITABLE_NUMBER_REGISTERS)

    coordinator = SprsunDataCoordinator(
        hass=hass,
        entry=entry,
        api=api,
        addresses=all_addresses,
        scan_interval=int(scan_interval),
        profile=str(profile),
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        await api.async_close()
        raise ConfigEntryNotReady(f"Initial Modbus refresh failed: {err}") from err

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_API: api,
        DATA_COORDINATOR: coordinator,
    }

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        entry_data = hass.data[DOMAIN].pop(entry.entry_id, None)
        if entry_data and DATA_API in entry_data:
            await entry_data[DATA_API].async_close()
    return unload_ok
