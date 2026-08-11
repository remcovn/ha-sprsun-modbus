"""Sensor platform for SPRSUN Modbus."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_COORDINATOR, DOMAIN, REG_UNIT_MODE
from .coordinator import SprsunDataCoordinator
from .register_definitions import OPTION_BY_UNIT_MODE, SENSOR_REGISTERS


@dataclass(frozen=True, kw_only=True)
class SprsunSensorEntityDescription(SensorEntityDescription):
    """SPRSUN sensor description."""

    address: int
    scale: float
    precision: int | None


SENSOR_DESCRIPTIONS: tuple[SprsunSensorEntityDescription, ...] = tuple(
    SprsunSensorEntityDescription(
        key=register.key,
        name=register.name,
        native_unit_of_measurement=register.unit,
        device_class=register.device_class,
        state_class=register.state_class,
        address=register.address,
        scale=register.scale,
        precision=register.precision,
    )
    for register in SENSOR_REGISTERS
)


class SprsunSensor(CoordinatorEntity[SprsunDataCoordinator], SensorEntity):
    """SPRSUN Modbus sensor entity."""

    entity_description: SprsunSensorEntityDescription

    def __init__(
        self,
        coordinator: SprsunDataCoordinator,
        entry: ConfigEntry,
        description: SprsunSensorEntityDescription,
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
    def native_value(self) -> float | int | None:
        """Return scaled sensor value from coordinator cache."""
        raw = self.coordinator.data.get(self.entity_description.address)
        if raw is None:
            return None

        value = raw * self.entity_description.scale
        if self.entity_description.precision is None:
            return value

        return round(value, self.entity_description.precision)


class SprsunUnitModeTextSensor(CoordinatorEntity[SprsunDataCoordinator], SensorEntity):
    """Human-readable text sensor derived from Unit Mode register."""

    _attr_name = "Unit Mode Text"
    _attr_has_entity_name = True
    _attr_icon = "mdi:hvac"

    def __init__(self, coordinator: SprsunDataCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_unit_mode_text"

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
    def native_value(self) -> str:
        """Return mapped text value for Unit Mode (P06)."""
        raw = self.coordinator.data.get(REG_UNIT_MODE)
        if raw is None:
            return "unknown"

        return OPTION_BY_UNIT_MODE.get(raw, f"Unknown ({raw})")


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SPRSUN sensor entities from a config entry."""
    coordinator: SprsunDataCoordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]

    entities = [SprsunSensor(coordinator, entry, description) for description in SENSOR_DESCRIPTIONS]
    entities.append(SprsunUnitModeTextSensor(coordinator, entry))
    async_add_entities(entities)
