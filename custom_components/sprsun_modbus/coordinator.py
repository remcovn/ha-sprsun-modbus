"""Coordinator for SPRSUN Modbus polling and writes."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import timedelta
import logging
import math

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import COORDINATOR_NAME, MAX_BACKOFF_SECONDS, REG_COMPRESSOR_FREQUENCY
from .modbus_api import SprsunModbusApi
from .register_definitions import POLL_INTERVAL_BY_ADDRESS, PROFILE_INTERVAL_MULTIPLIER

_LOGGER = logging.getLogger(__name__)


def _to_int16(raw: int) -> int:
    """Convert unsigned 16-bit value to signed int16."""
    return raw - 65536 if raw > 32767 else raw


def _group_contiguous(addresses: Iterable[int], max_block: int = 25) -> list[tuple[int, int]]:
    """Group sorted addresses into contiguous blocks."""
    sorted_addresses = sorted(set(addresses))
    if not sorted_addresses:
        return []

    blocks: list[tuple[int, int]] = []
    start = sorted_addresses[0]
    prev = start

    for address in sorted_addresses[1:]:
        if address == prev + 1 and (address - start + 1) <= max_block:
            prev = address
            continue

        blocks.append((start, prev - start + 1))
        start = address
        prev = address

    blocks.append((start, prev - start + 1))
    return blocks


class SprsunDataCoordinator(DataUpdateCoordinator[dict[int, int]]):
    """Coordinate Modbus polling and writes for SPRSUN."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api: SprsunModbusApi,
        addresses: Iterable[int],
        scan_interval: int,
        profile: str,
    ) -> None:
        self._base_scan_interval = max(1, int(scan_interval))
        super().__init__(
            hass,
            _LOGGER,
            name=COORDINATOR_NAME,
            update_interval=timedelta(seconds=self._base_scan_interval),
        )
        self.entry = entry
        self.api = api
        self.addresses = sorted(set(addresses))
        self.profile = profile
        self._profile_multiplier = PROFILE_INTERVAL_MULTIPLIER.get(profile, 1.0)
        self._tick = 0
        self._cached_values: dict[int, int] = {}
        self._failure_count = 0

    def _interval_ticks_for_address(self, address: int) -> int:
        """Compute poll cadence in ticks for an address based on selected profile."""
        base_interval = POLL_INTERVAL_BY_ADDRESS.get(address, 30)
        adjusted_seconds = max(1.0, float(base_interval) * self._profile_multiplier)
        ticks = max(1, math.ceil(adjusted_seconds / self._base_scan_interval))
        return ticks

    def _addresses_for_current_tick(self) -> list[int]:
        """Return addresses that should be refreshed on the current scheduler tick."""
        due: list[int] = []
        for address in self.addresses:
            interval_ticks = self._interval_ticks_for_address(address)
            if self._tick % interval_ticks == 0:
                due.append(address)
        return due

    def _set_backoff_interval(self, failure_count: int) -> None:
        """Adjust coordinator polling interval with exponential backoff."""
        factor = 2 ** max(0, failure_count - 1)
        seconds = min(MAX_BACKOFF_SECONDS, int(self._base_scan_interval * factor))
        self.update_interval = timedelta(seconds=max(1, seconds))

    def _reset_backoff_interval(self) -> None:
        """Restore base polling interval after successful update."""
        self.update_interval = timedelta(seconds=self._base_scan_interval)

    async def _async_update_data(self) -> dict[int, int]:
        """Fetch fresh data from Modbus in profile-based register groups."""
        self._tick += 1
        due_addresses = self._addresses_for_current_tick()
        if not due_addresses:
            return dict(self._cached_values)

        try:
            for start, count in _group_contiguous(due_addresses):
                registers = await self.api.async_read_holding_block(start, count)
                for offset, raw in enumerate(registers):
                    self._cached_values[start + offset] = _to_int16(raw)

            self._failure_count = 0
            self._reset_backoff_interval()
        except Exception as err:
            self._failure_count += 1
            self._set_backoff_interval(self._failure_count)
            raise UpdateFailed(f"Modbus update failed: {err}") from err

        return dict(self._cached_values)

    async def async_write_register(self, address: int, value: int) -> None:
        """Write register and request refresh afterwards."""
        await self.api.async_write_register(address=address, value=value)
        await self.async_request_refresh()

    def compressor_frequency(self) -> float | None:
        """Return compressor frequency in Hz."""
        raw = self.data.get(REG_COMPRESSOR_FREQUENCY) if self.data else None
        if raw is None:
            return None
        return float(raw)
