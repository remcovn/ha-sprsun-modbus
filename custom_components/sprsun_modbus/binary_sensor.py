"""Binary sensor platform for SPRSUN Modbus status bits."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_COORDINATOR, DOMAIN
from .coordinator import SprsunDataCoordinator
from .register_definitions import BINARY_SENSOR_REGISTERS


@dataclass(frozen=True, kw_only=True)
class SprsunBinarySensorEntityDescription(BinarySensorEntityDescription):
    """SPRSUN binary sensor description."""

    address: int
    bitmask: int


class SprsunBinarySensor(
    CoordinatorEntity[SprsunDataCoordinator],
    BinarySensorEntity,
):
    """Binary sensor representing one bit in a SPRSUN status register."""

    entity_description: SprsunBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: SprsunDataCoordinator,
        entry: ConfigEntry,
        description: SprsunBinarySensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._entry = entry
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

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
    def is_on(self) -> bool | None:
        """Return whether this status bit is set."""
        raw = self.coordinator.data.get(self.entity_description.address)
        if raw is None:
            return None

        return bool(raw & self.entity_description.bitmask)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SPRSUN status-bit binary sensors from a config entry."""
    coordinator: SprsunDataCoordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]

    entities = [
        SprsunBinarySensor(
            coordinator,
            entry,
            SprsunBinarySensorEntityDescription(
                key=register.key,
                name=register.name,
                address=register.address,
                bitmask=register.bitmask,
            ),
        )
        for register in BINARY_SENSOR_REGISTERS
    ]
    async_add_entities(entities)
