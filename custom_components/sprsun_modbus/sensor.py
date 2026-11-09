"""Sensor platform for SPRSUN Modbus."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_EST_COMPRESSOR_BASE_W,
    CONF_EST_COMPRESSOR_W_PER_HZ,
    CONF_EST_PUMP_W_PER_PCT,
    CONF_EST_STANDBY_W,
    DATA_COORDINATOR,
    DEFAULT_EST_COMPRESSOR_BASE_W,
    DEFAULT_EST_COMPRESSOR_W_PER_HZ,
    DEFAULT_EST_PUMP_W_PER_PCT,
    DEFAULT_EST_STANDBY_W,
    DOMAIN,
    REG_COMPRESSOR_FREQUENCY,
    REG_PUMP_PWM,
    REG_UNIT_MODE,
)
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


class SprsunEstimatedPowerSensor(CoordinatorEntity[SprsunDataCoordinator], SensorEntity):
    """Modelled electrical power; the heat pump has no usable power register."""

    _attr_name = "Estimated Power"
    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_icon = "mdi:flash-triangle-outline"
    _unrecorded_attributes = frozenset(
        {
            "estimated",
            "model",
            "standby_w",
            "compressor_base_w",
            "compressor_w_per_hz",
            "pump_w_per_pct",
        }
    )

    def __init__(self, coordinator: SprsunDataCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_estimated_power"
        options = entry.options
        self._standby_w = float(options.get(CONF_EST_STANDBY_W, DEFAULT_EST_STANDBY_W))
        self._compressor_base_w = float(options.get(CONF_EST_COMPRESSOR_BASE_W, DEFAULT_EST_COMPRESSOR_BASE_W))
        self._compressor_w_per_hz = float(
            options.get(CONF_EST_COMPRESSOR_W_PER_HZ, DEFAULT_EST_COMPRESSOR_W_PER_HZ)
        )
        self._pump_w_per_pct = float(options.get(CONF_EST_PUMP_W_PER_PCT, DEFAULT_EST_PUMP_W_PER_PCT))
        self._attr_extra_state_attributes = {
            "estimated": True,
            "model": "standby + pump_w_per_pct * pump_pwm + (compressor_base_w + compressor_w_per_hz * frequency if frequency > 0)",
            "standby_w": self._standby_w,
            "compressor_base_w": self._compressor_base_w,
            "compressor_w_per_hz": self._compressor_w_per_hz,
            "pump_w_per_pct": self._pump_w_per_pct,
        }

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
        """Return estimated power from compressor frequency and pump PWM."""
        frequency = self.coordinator.data.get(REG_COMPRESSOR_FREQUENCY)
        pump_pwm = self.coordinator.data.get(REG_PUMP_PWM)
        if frequency is None or pump_pwm is None:
            return None

        power = self._standby_w + self._pump_w_per_pct * max(0, pump_pwm)
        if frequency > 0:
            power += self._compressor_base_w + self._compressor_w_per_hz * frequency
        return round(power)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SPRSUN sensor entities from a config entry."""
    coordinator: SprsunDataCoordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]

    entities = [SprsunSensor(coordinator, entry, description) for description in SENSOR_DESCRIPTIONS]
    entities.append(SprsunUnitModeTextSensor(coordinator, entry))
    entities.append(SprsunEstimatedPowerSensor(coordinator, entry))
    async_add_entities(entities)
