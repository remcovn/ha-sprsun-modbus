"""Select platform for SPRSUN mode selection."""

from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_COORDINATOR, DOMAIN, REG_UNIT_MODE
from .coordinator import SprsunDataCoordinator
from .register_definitions import OPTION_BY_UNIT_MODE, UNIT_MODE_BY_OPTION

_LOGGER = logging.getLogger(__name__)


class SprsunUnitModeSelect(CoordinatorEntity[SprsunDataCoordinator], SelectEntity):
    """Select entity for unit mode register P06."""

    _attr_name = "Unit Mode"
    _attr_has_entity_name = True
    _attr_options = list(UNIT_MODE_BY_OPTION.keys())

    def __init__(self, coordinator: SprsunDataCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_unit_mode"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for registry."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="SPRSUN Heat Pump",
            manufacturer="SPRSUN",
            model="Modbus Heat Pump",
        )

    @property
    def current_option(self) -> str | None:
        """Return current mapped mode option."""
        raw = self.coordinator.data.get(REG_UNIT_MODE)
        if raw is None:
            return None

        return OPTION_BY_UNIT_MODE.get(raw)

    async def async_select_option(self, option: str) -> None:
        """Write selected unit mode with safety guard."""
        if option not in UNIT_MODE_BY_OPTION:
            raise HomeAssistantError(f"Unsupported unit mode option: {option}")

        compressor_frequency = self.coordinator.compressor_frequency()
        if compressor_frequency is None:
            raise HomeAssistantError("Compressor frequency is unavailable; mode write blocked")

        if compressor_frequency > 0:
            _LOGGER.warning(
                "Blocked Unit Mode write because compressor frequency is %.1f Hz",
                compressor_frequency,
            )
            raise HomeAssistantError(
                "Unit mode change blocked: compressor is running"
            )

        await self.coordinator.async_write_register(REG_UNIT_MODE, UNIT_MODE_BY_OPTION[option])


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SPRSUN select entities from a config entry."""
    coordinator: SprsunDataCoordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    async_add_entities([SprsunUnitModeSelect(coordinator, entry)])
