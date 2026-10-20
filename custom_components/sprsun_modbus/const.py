"""Constants for the SPRSUN Modbus integration."""

DOMAIN = "sprsun_modbus"
PLATFORMS = ["sensor", "binary_sensor", "number", "select"]

CONF_HOST = "host"
CONF_PORT = "port"
CONF_SLAVE = "slave"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_PROFILE = "profile"

DEFAULT_PORT = 8899
DEFAULT_SLAVE = 1
DEFAULT_SCAN_INTERVAL = 15
DEFAULT_PROFILE = "balanced"

PROFILE_FAST = "fast"
PROFILE_BALANCED = "balanced"
PROFILE_CONSERVATIVE = "conservative"
PROFILE_OPTIONS = [PROFILE_FAST, PROFILE_BALANCED, PROFILE_CONSERVATIVE]

MAX_BACKOFF_SECONDS = 300

COORDINATOR_NAME = "sprsun_modbus_coordinator"

DATA_COORDINATOR = "coordinator"
DATA_API = "api"

REG_COMPRESSOR_FREQUENCY = 30
REG_UNIT_MODE = 54
