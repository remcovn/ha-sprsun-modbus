"""Register and entity definitions for SPRSUN v1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SensorRegister:
    """Definition for a read-only sensor register."""

    key: str
    name: str
    address: int
    scale: float = 1.0
    precision: int | None = None
    unit: str | None = None
    device_class: str | None = None
    state_class: str | None = "measurement"


@dataclass(frozen=True)
class WritableNumberRegister:
    """Definition for writable number register entities."""

    key: str
    name: str
    address: int
    min_value: float
    max_value: float
    step: float
    unit: str
    write_scale: float


POLL_INTERVAL_BY_ADDRESS: dict[int, int] = {
    14: 15,
    15: 15,
    17: 15,
    18: 15,
    21: 15,
    22: 15,
    27: 15,
    28: 15,
    30: 15,
    33: 15,
    34: 15,
    35: 15,
    36: 15,
    38: 15,
    39: 15,
    40: 15,
    41: 15,
    46: 15,
    47: 15,
    48: 15,
    54: 30,
    198: 30,
    199: 30,
    200: 30,
    201: 30,
    202: 30,
    203: 30,
    204: 30,
    205: 60,
    206: 60,
    207: 60,
    208: 60,
    209: 15,
    210: 15,
    211: 15,
    215: 30,
    216: 30,
    217: 30,
    385: 60,
    386: 60,
    387: 60,
    388: 60,
    389: 60,
    390: 30,
    391: 30,
    392: 30,
    393: 30,
    394: 30,
    395: 60,
    396: 60,
    397: 60,
    398: 30,
    399: 60,
    401: 60,
    402: 60,
    403: 60,
    404: 60,
    405: 60,
    406: 60,
    407: 60,
    408: 60,
    409: 60,
    415: 30,
    416: 30,
    417: 30,
    418: 30,
    419: 30,
    434: 60,
    435: 60,
    436: 60,
    438: 60,
    439: 60,
    440: 60,
    441: 60,
    442: 300,
    44: 120,
    45: 120,
}


PROFILE_INTERVAL_MULTIPLIER: dict[str, float] = {
    "fast": 0.75,
    "balanced": 1.0,
    "conservative": 1.5,
}


SENSOR_REGISTERS: tuple[SensorRegister, ...] = (
    SensorRegister("inlet_temperature", "Inlet Temperature", 14, scale=0.1, precision=1, unit="°C", device_class="temperature"),
    SensorRegister("hot_water_temperature", "Hot Water Temperature", 15, scale=0.1, precision=1, unit="°C", device_class="temperature"),
    SensorRegister("ambient_temperature", "Ambient Temperature", 17, scale=0.5, precision=1, unit="°C", device_class="temperature"),
    SensorRegister("outlet_temperature", "Outlet Temperature", 18, scale=0.1, precision=1, unit="°C", device_class="temperature"),
    SensorRegister("suction_gas_temperature", "Suction Gas Temperature", 21, scale=0.5, precision=1, unit="°C", device_class="temperature"),
    SensorRegister("coil_temperature", "Coil Temperature", 22, scale=0.5, precision=1, unit="°C", device_class="temperature"),
    SensorRegister("exhaust_temperature", "Exhaust Temperature", 27, scale=1.0, precision=0, unit="°C", device_class="temperature"),
    SensorRegister("eev1_opening_step", "EEV1 Opening Step", 28, precision=0),
    SensorRegister("compressor_frequency", "Compressor Frequency", 30, precision=0, unit="Hz"),
    SensorRegister("sprsun_input_power", "SPRSUN Input Power", 33, precision=0, unit="W", device_class="power"),
    SensorRegister("sprsun_inverter_voltage", "SPRSUN Inverter Voltage", 34, precision=0, unit="V", device_class="voltage"),
    SensorRegister("sprsun_inverter_current", "SPRSUN Inverter Current", 35, precision=0, unit="A", device_class="current"),
    SensorRegister("compressor_target_frequency", "Compressor Target Frequency", 36, precision=0, unit="Hz"),
    SensorRegister("dc_fan_1_speed", "DC Fan 1 Speed", 38, precision=0, unit="rpm"),
    SensorRegister("dc_fan_2_speed", "DC Fan 2 Speed", 39, precision=0, unit="rpm"),
    SensorRegister("evaporator_temperature", "Evaporator Temperature", 40, scale=0.1, precision=1, unit="°C", device_class="temperature"),
    SensorRegister("condenser_temperature", "Condenser Temperature", 41, scale=0.1, precision=1, unit="°C", device_class="temperature"),
    SensorRegister("controller_version", "Controller Version", 44, precision=0, state_class=None),
    SensorRegister("display_version", "Display Version", 45, precision=0, state_class=None),
    SensorRegister("pump_pwm", "Pump PWM", 46, precision=0, unit="%"),
    SensorRegister("suction_pressure", "Suction Pressure", 47, scale=0.01, precision=2, unit="bar"),
    SensorRegister("discharge_pressure", "Discharge Pressure", 48, scale=0.01, precision=2, unit="bar"),
    SensorRegister("unit_mode_p06", "Unit Mode (P06)", 54, precision=0, state_class=None),
    SensorRegister("heat_delta_temp", "Heat Delta Temp", 198, precision=0, unit="°C"),
    SensorRegister("ac_constant_temp_diff", "AC Constant Temp Diff", 199, precision=0, unit="°C"),
    SensorRegister("hot_water_delta_temp", "Hot Water Delta Temp", 200, precision=0, unit="°C"),
    SensorRegister("wt_constant_temp_diff", "WT Constant Temp Diff", 201, precision=0, unit="°C"),
    SensorRegister("hot_water_setpoint", "Hot Water Setpoint", 202, scale=0.5, precision=1, unit="°C", device_class="temperature"),
    SensorRegister("cooling_setpoint", "Cooling Setpoint", 203, scale=0.5, precision=1, unit="°C", device_class="temperature"),
    SensorRegister("heating_setpoint", "Heating Setpoint", 204, scale=0.5, precision=1, unit="°C", device_class="temperature"),
    SensorRegister("wt_temp_calibration_f44", "WT Temp Calibration (F44)", 205, precision=0, unit="°C"),
    SensorRegister("inlet_temp_calibration_f45", "Inlet Temp Calibration (F45)", 206, precision=0, unit="°C"),
    SensorRegister("outlet_temp_calibration_f46", "Outlet Temp Calibration (F46)", 207, precision=0, unit="°C"),
    SensorRegister("wt_temp_offset_setpoint_f49", "WT Temp Offset Setpoint (F49)", 208, precision=0, unit="°C"),
    SensorRegister("status_field_a", "Status Field A", 209, precision=0, state_class=None),
    SensorRegister("protection_code", "Protection Code", 210, precision=0, state_class=None),
    SensorRegister("suction_superheat", "Suction Superheat", 211, precision=0, unit="K"),
    SensorRegister("defrost_field_1", "Defrost Field 1", 215, precision=0, state_class=None),
    SensorRegister("defrost_field_2", "Defrost Field 2", 216, precision=0, state_class=None),
    SensorRegister("defrost_field_3", "Defrost Field 3", 217, precision=0, state_class=None),
    SensorRegister("comp_delay_g08", "Comp Delay (G08)", 385, precision=0, unit="min"),
    SensorRegister("comp_delay_g06", "Comp Delay (G06)", 386, precision=0, unit="min"),
    SensorRegister("hot_water_heater_ext_g07", "Hot Water Heater Ext (G07)", 387, precision=0, unit="°C"),
    SensorRegister("heating_heater_ext_g05", "Heating Heater Ext (G05)", 388, precision=0, unit="°C"),
    SensorRegister("start_internal_g03", "Start Internal (G03)", 389, precision=0, unit="min"),
    SensorRegister("dc_pump_mode_f13", "DC Pump Mode (F13)", 390, precision=0, state_class=None),
    SensorRegister("dc_pump_cycle_f14", "DC Pump Cycle (F14)", 391, precision=0, unit="s"),
    SensorRegister("dc_pump_freq_set_f15", "DC Pump Freq Set (F15)", 392, precision=0, unit="%"),
    SensorRegister("dc_pump_max_freq_f16", "DC Pump Max Freq (F16)", 393, precision=0, unit="%"),
    SensorRegister("dc_pump_min_freq_f17", "DC Pump Min Freq (F17)", 394, precision=0, unit="%"),
    SensorRegister("dc_pump_scale_factor_f18", "DC Pump Scale Factor (F18)", 395, precision=0, state_class=None),
    SensorRegister("dc_pump_diff_f19", "DC Pump Diff (F19)", 396, precision=0, state_class=None),
    SensorRegister("delta_temp_set_g04", "Delta Temp Set (G04)", 397, precision=0, unit="°C"),
    SensorRegister("pump_work_mode_g02", "Pump Work Mode (G02)", 398, precision=0, state_class=None),
    SensorRegister("comp_freq_diff_f22", "Comp Freq Diff (F22)", 399, precision=0, state_class=None),
    SensorRegister("enable_switch_amb_linkage_g09", "Enable Switch Amb Linkage (G09)", 401, precision=0, state_class=None),
    SensorRegister("ambient_temp_switch_setpoint_g10", "Ambient Temp Switch Setpoint (G10)", 402, precision=0, unit="°C"),
    SensorRegister("ambient_temp_diff_g11", "Ambient Temp Diff (G11)", 403, precision=0, unit="°C"),
    SensorRegister("limit_freq_temp_diff_f27", "Limit Freq Temp Diff (F27)", 404, precision=0, unit="°C"),
    SensorRegister("decrease_freq_temp_diff_f28", "Decrease Freq Temp Diff (F28)", 405, precision=0, unit="°C"),
    SensorRegister("limit_freq_outlet_low_f29", "Limit Freq Outlet Low (F29)", 406, precision=0, unit="°C"),
    SensorRegister("decrease_freq_outlet_low_f30", "Decrease Freq Outlet Low (F30)", 407, precision=0, unit="°C"),
    SensorRegister("limit_freq_outlet_high_f31", "Limit Freq Outlet High (F31)", 408, precision=0, unit="°C"),
    SensorRegister("decrease_freq_outlet_high_f32", "Decrease Freq Outlet High (F32)", 409, precision=0, unit="°C"),
    SensorRegister("antifreeze_cycle_f35", "Antifreeze Cycle (F35)", 415, precision=0, unit="min"),
    SensorRegister("three_way_valve_cycle_f36", "Three-way Valve Cycle (F36)", 416, precision=0, unit="hour"),
    SensorRegister("pump_cycle_in_error_f37", "Pump Cycle In Error (F37)", 417, precision=0, unit="min"),
    SensorRegister("comp_freq_cycle_f38", "Comp Freq Cycle (F38)", 418, precision=0, unit="s"),
    SensorRegister("air_too_low_setpoint_f41", "Air Too Low Setpoint (F41)", 419, precision=0, unit="°C"),
    SensorRegister("high_pressure_adjust_f47", "High Pressure Adjust (F47)", 434, precision=0, state_class=None),
    SensorRegister("low_pressure_adjust_f48", "Low Pressure Adjust (F48)", 435, precision=0, state_class=None),
    SensorRegister("air_too_low_diff_f51", "Air Too Low Diff (F51)", 436, precision=0, unit="°C"),
    SensorRegister("outlet_temp_offset_setpoint_f53", "Outlet Temp Offset Setpoint (F53)", 438, precision=0, unit="°C"),
    SensorRegister("outlet_temp_offset_f52", "Outlet Temp Offset (F52)", 439, precision=0, unit="°C"),
    SensorRegister("heat_upper_limit_setpoint_f54", "Heat Upper Limit Setpoint (F54)", 440, precision=0, unit="°C"),
    SensorRegister("cool_lower_limit_setpoint_f55", "Cool Lower Limit Setpoint (F55)", 441, precision=0, unit="°C"),
    SensorRegister("model_selection_f56", "Model Selection (F56)", 442, precision=0, state_class=None),
)


WRITABLE_NUMBER_REGISTERS: tuple[WritableNumberRegister, ...] = (
    WritableNumberRegister(
        key="sprsun_hot_water_setpoint",
        name="SPRSUN Hot Water Setpoint",
        address=202,
        min_value=30,
        max_value=60,
        step=0.5,
        unit="°C",
        write_scale=2,
    ),
    WritableNumberRegister(
        key="sprsun_cooling_setpoint",
        name="SPRSUN Cooling Setpoint",
        address=203,
        min_value=7,
        max_value=30,
        step=0.5,
        unit="°C",
        write_scale=2,
    ),
    WritableNumberRegister(
        key="sprsun_heating_setpoint",
        name="SPRSUN Heating Setpoint",
        address=204,
        min_value=20,
        max_value=55,
        step=0.5,
        unit="°C",
        write_scale=2,
    ),
    WritableNumberRegister(
        key="sprsun_heat_delta_temp",
        name="SPRSUN Heat Delta Temp",
        address=198,
        min_value=1,
        max_value=20,
        step=1,
        unit="°C",
        write_scale=1,
    ),
    WritableNumberRegister(
        key="sprsun_ac_constant_temp_diff",
        name="SPRSUN AC Constant Temp Diff",
        address=199,
        min_value=1,
        max_value=20,
        step=1,
        unit="°C",
        write_scale=1,
    ),
    WritableNumberRegister(
        key="sprsun_hot_water_delta_temp",
        name="SPRSUN Hot Water Delta Temp",
        address=200,
        min_value=1,
        max_value=20,
        step=1,
        unit="°C",
        write_scale=1,
    ),
)


UNIT_MODE_BY_OPTION: dict[str, int] = {
    "DHW": 0,
    "Heating": 1,
    "Cooling": 2,
    "Heating + DHW": 3,
    "Cooling + DHW": 4,
}

OPTION_BY_UNIT_MODE: dict[int, str] = {value: key for key, value in UNIT_MODE_BY_OPTION.items()}
