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
REG_PUMP_PWM = 46
REG_UNIT_MODE = 54

# Estimated power model, calibrated against a smart meter (1-phase 230 V).
CONF_EST_STANDBY_W = "est_standby_w"
CONF_EST_COMPRESSOR_BASE_W = "est_compressor_base_w"
CONF_EST_COMPRESSOR_W_PER_HZ = "est_compressor_w_per_hz"
CONF_EST_PUMP_W_PER_PCT = "est_pump_w_per_pct"

DEFAULT_EST_STANDBY_W = 30.0
DEFAULT_EST_COMPRESSOR_BASE_W = 265.0
DEFAULT_EST_COMPRESSOR_W_PER_HZ = 25.4
DEFAULT_EST_PUMP_W_PER_PCT = 0.69
