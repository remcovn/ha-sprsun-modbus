"""Number platform for SPRSUN writable setpoints."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.number import NumberEntity, NumberEntityDescription, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_COORDINATOR, DOMAIN
from .coordinator import SprsunDataCoordinator
from .register_definitions import WRITABLE_NUMBER_REGISTERS


@dataclass(frozen=True, kw_only=True)
class SprsunNumberEntityDescription(NumberEntityDescription):
    """SPRSUN writable number description."""

    address: int
    write_scale: float


NUMBER_DESCRIPTIONS: tuple[SprsunNumberEntityDescription, ...] = tuple(
    SprsunNumberEntityDescription(
        key=register.key,
        name=register.name,
        native_min_value=register.min_value,
        native_max_value=register.max_value,
        native_step=register.step,
        native_unit_of_measurement=register.unit,
        mode=NumberMode.BOX,
        address=register.address,
        write_scale=register.write_scale,
    )
    for register in WRITABLE_NUMBER_REGISTERS
)


class SprsunWritableNumber(CoordinatorEntity[SprsunDataCoordinator], NumberEntity):
    """Writable number entity backed by a Modbus register."""

    entity_description: SprsunNumberEntityDescription

    def __init__(
        self,
        coordinator: SprsunDataCoordinator,
        entry: ConfigEntry,
        description: SprsunNumberEntityDescription,
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
    def native_value(self) -> float | None:
        """Return current scaled value from coordinator data."""
        raw = self.coordinator.data.get(self.entity_description.address)
        if raw is None:
            return None

        return round(float(raw) / self.entity_description.write_scale, 2)

    async def async_set_native_value(self, value: float) -> None:
        """Write value to the underlying Modbus register."""
        register_value = int(round(value * self.entity_description.write_scale))
        await self.coordinator.async_write_register(self.entity_description.address, register_value)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SPRSUN number entities from a config entry."""
    coordinator: SprsunDataCoordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]

    async_add_entities(
        SprsunWritableNumber(coordinator, entry, description) for description in NUMBER_DESCRIPTIONS
    )
