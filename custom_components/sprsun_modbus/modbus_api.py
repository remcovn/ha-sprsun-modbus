"""Pymodbus API wrapper for SPRSUN."""

from __future__ import annotations

from asyncio import Lock
import logging

from pymodbus.client import AsyncModbusTcpClient

_LOGGER = logging.getLogger(__name__)


class SprsunModbusApi:
    """Minimal async API wrapper around pymodbus."""

    def __init__(self, host: str, port: int, slave: int, timeout: int = 5) -> None:
        self._host = host
        self._port = port
        self._slave = slave
        self._timeout = timeout
        self._client = AsyncModbusTcpClient(host=host, port=port, timeout=timeout)
        self._lock = Lock()

    async def async_close(self) -> None:
        """Close the TCP client connection."""
        self._client.close()

    async def _async_ensure_connected(self) -> None:
        """Ensure the pymodbus client is connected."""
        if self._client.connected:
            return

        connected = await self._client.connect()
        if not connected:
            raise ConnectionError(f"Unable to connect to Modbus endpoint {self._host}:{self._port}")

    async def async_read_holding_block(self, address: int, count: int) -> list[int]:
        """Read a contiguous holding-register block."""
        async with self._lock:
            await self._async_ensure_connected()

            response = await self._client.read_holding_registers(
                address=address,
                count=count,
                device_id=self._slave,
            )

            if response.isError():
                raise RuntimeError(f"Modbus read failed at address {address}, count {count}: {response}")

            if not hasattr(response, "registers"):
                raise RuntimeError(f"Modbus read returned no registers for {address}:{count}")

            return list(response.registers)

    async def async_write_register(self, address: int, value: int) -> None:
        """Write a single holding register."""
        async with self._lock:
            await self._async_ensure_connected()

            _LOGGER.debug("Writing register %s=%s", address, value)
            response = await self._client.write_register(
                address=address,
                value=value,
                device_id=self._slave,
            )

            if response.isError():
                raise RuntimeError(f"Modbus write failed at address {address} value {value}: {response}")
