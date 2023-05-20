"""Home Assistant sensor descriptions."""
from __future__ import annotations

from collections.abc import Mapping

from typing import Any

from givenergy_modbus.model.inverter import Model
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ELECTRIC_POTENTIAL_VOLT,
    ENERGY_KILO_WATT_HOUR,
    FREQUENCY_HERTZ,
    PERCENTAGE,
    POWER_WATT,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN, LOGGER, Icon
from .coordinator import GivEnergyUpdateCoordinator
from .entity import BatteryEntity, InverterEntity

_BASIC_INVERTER_SENSORS = [
    SensorEntityDescription(
        key="e_pv_total",
        name="PV Energy Total",
        icon=Icon.PV,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="p_pv1",
        name="PV Power (String 1)",
        icon=Icon.PV,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=POWER_WATT,
    ),
    SensorEntityDescription(
        key="p_pv2",
        name="PV Power (String 2)",
        icon=Icon.PV,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=POWER_WATT,
    ),
    SensorEntityDescription(
        key="e_grid_in_day",
        name="Grid Import Today",
        icon=Icon.GRID_IMPORT,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="e_grid_in_total",
        name="Grid Import Total",
        icon=Icon.GRID_IMPORT,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="e_grid_out_day",
        name="Grid Export Today",
        icon=Icon.GRID_EXPORT,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="e_grid_out_total",
        name="Grid Export Total",
        icon=Icon.GRID_EXPORT,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="e_inverter_out_day",
        name="Inverter Output Today",
        icon=Icon.INVERTER,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="e_inverter_out_total",
        name="Inverter Output Total",
        icon=Icon.INVERTER,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="e_battery_charge_day",
        name="Battery Charge Today",
        icon=Icon.BATTERY_PLUS,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="e_battery_discharge_day",
        name="Battery Discharge Today",
        icon=Icon.BATTERY_MINUS,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="e_battery_throughput_total",
        name="Battery Throughput Total",
        icon=Icon.BATTERY,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="p_load_demand",
        name="Consumption Power",
        icon=Icon.AC,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=POWER_WATT,
    ),
    SensorEntityDescription(
        key="p_grid_out",
        name="Grid Power",
        icon=Icon.GRID_EXPORT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=POWER_WATT,
    ),
    SensorEntityDescription(
        key="v_battery",
        name="Battery Voltage",
        icon=Icon.BATTERY,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
    ),
    SensorEntityDescription(
        key="p_battery",
        name="Battery Power",
        icon=Icon.BATTERY,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=POWER_WATT,
    ),
    SensorEntityDescription(
        key="p_eps_backup",
        name="Inverter EPS Backup Power",
        icon=Icon.AC,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=POWER_WATT,
    ),
    SensorEntityDescription(
        key="battery_percent",
        name="Battery Percent",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        key="temp_battery",
        name="Battery Temperature",
        icon=Icon.BATTERY_TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
    SensorEntityDescription(
        key="v_ac1",
        name="Grid Voltage",
        icon=Icon.AC,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
    ),
    SensorEntityDescription(
        key="f_ac1",
        name="Grid Frequency",
        icon=Icon.AC,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=FREQUENCY_HERTZ,
    ),
    SensorEntityDescription(
        key="temp_inverter_heatsink",
        name="Inverter Heatsink Temperature",
        icon=Icon.TEMPERATURE,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
    SensorEntityDescription(
        key="temp_charger",
        name="Inverter Charger Temperature",
        icon=Icon.TEMPERATURE,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
]

_PV_ENERGY_TODAY_SENSOR = SensorEntityDescription(
    key="e_pv_day",
    name="PV Energy Today",
    icon=Icon.PV,
    device_class=SensorDeviceClass.ENERGY,
    state_class=SensorStateClass.TOTAL_INCREASING,
    native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
)

_PV_POWER_SENSOR = SensorEntityDescription(
    key="p_pv",
    name="PV Power",
    icon=Icon.PV,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=POWER_WATT,
)

_CONSUMPTION_TODAY_SENSOR = SensorEntityDescription(
    key="e_consumption_today",
    name="Consumption Today",
    icon=Icon.AC,
    device_class=SensorDeviceClass.ENERGY,
    state_class=SensorStateClass.TOTAL_INCREASING,
    native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
)

_CONSUMPTION_TOTAL_SENSOR = SensorEntityDescription(
    key="e_consumption_consumption",
    name="Consumption Total",
    icon=Icon.AC,
    device_class=SensorDeviceClass.ENERGY,
    state_class=SensorStateClass.TOTAL_INCREASING,
    native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
)

_GRID_IMPORT_POWER = SensorEntityDescription(
    key="p_grid_import_power",
    name="Grid Import Power",
    icon=Icon.GRID_IMPORT,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=POWER_WATT,
)

_GRID_EXPORT_POWER = SensorEntityDescription(
    key="p_grid_export_power",
    name="Grid Export Power",
    icon=Icon.GRID_EXPORT,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=POWER_WATT,
)

_BATTERY_MODE_SENSOR = SensorEntityDescription(
    key="battery_mode_description",
    name="Battery Mode",
    icon=Icon.BATTERY,
)

_BASIC_BATTERY_SENSORS = [
    SensorEntityDescription(
        key="battery_soc",
        name="Battery Charge",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        key="battery_num_cycles",
        name="Battery Cycles",
        icon=Icon.BATTERY_CYCLES,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="v_battery_out",
        name="Battery Output Voltage",
        icon=Icon.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
    ),
]

_BATTERY_REMAINING_CAPACITY_SENSOR = SensorEntityDescription(
    key="battery_remaining_capacity",
    name="Battery Remaining Capacity",
    icon=Icon.BATTERY,
    device_class=SensorDeviceClass.ENERGY,
    state_class=SensorStateClass.TOTAL,
    native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
)

_BATTERY_CELLS_VOLTAGE_SENSOR = SensorEntityDescription(
    key="v_battery_cells_sum",
    name="Battery Cells Voltage",
    icon=Icon.BATTERY,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
)

_SOLAR_TO_HOUSE = SensorEntityDescription(
    key="solar_to_house",
    name="Solar to House",
    icon=Icon.PV,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=POWER_WATT,
)

_SOLAR_TO_BATTERY = SensorEntityDescription(
    key="solar_to_battery",
    name="Solar to Battery",
    icon=Icon.PV,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=POWER_WATT,
)

_SOLAR_TO_GRID = SensorEntityDescription(
    key="solar_to_grid",
    name="Solar to Grid",
    icon=Icon.PV,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=POWER_WATT,
)

_BATTERY_TO_HOUSE = SensorEntityDescription(
    key="battery_to_house",
    name="Battery to House",
    icon=Icon.BATTERY,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=POWER_WATT,
)

_BATTERY_TO_GRID = SensorEntityDescription(
    key="battery_to_grid",
    name="Battery to Grid",
    icon=Icon.BATTERY,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=POWER_WATT,
)

_GRID_TO_BATTERY = SensorEntityDescription(
    key="grid_to_battery",
    name="Grid to Battery",
    icon=Icon.GRID_IMPORT,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=POWER_WATT,
)

_GRID_TO_HOUSE = SensorEntityDescription(
    key="grid_to_house",
    name="Grid to House",
    icon=Icon.GRID_IMPORT,
    device_class=SensorDeviceClass.POWER,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=POWER_WATT,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    coordinator: GivEnergyUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []

    # Add basic inverter sensors that map directly to registers.
    entities.extend(
        [
            InverterBasicSensor(coordinator, config_entry, entity_description)
            for entity_description in _BASIC_INVERTER_SENSORS
        ]
    )

    # Add other inverter sensors that require more customization
    # (e.g. sensors that derive values from several registers).
    entities.extend(
        [
            PVEnergyTodaySensor(
                coordinator, config_entry, entity_description=_PV_ENERGY_TODAY_SENSOR
            ),
            PVPowerSensor(
                coordinator, config_entry, entity_description=_PV_POWER_SENSOR
            ),
            ConsumptionTodaySensor(
                coordinator, config_entry, entity_description=_CONSUMPTION_TODAY_SENSOR
            ),
            ConsumptionTotalSensor(
                coordinator, config_entry, entity_description=_CONSUMPTION_TOTAL_SENSOR
            ),
            GridImportPower(
                coordinator, config_entry, entity_description=_GRID_IMPORT_POWER
            ),
            GridExportPower(
                coordinator, config_entry, entity_description=_GRID_EXPORT_POWER
            ),
            BatteryModeSensor(
                coordinator, config_entry, entity_description=_BATTERY_MODE_SENSOR
            ),
            SolarToHouse(
                coordinator, config_entry, entity_description=_SOLAR_TO_HOUSE
            ),
            SolarToBattery(
                coordinator, config_entry, entity_description=_SOLAR_TO_BATTERY
            ),
            SolarToGrid(
                coordinator, config_entry, entity_description=_SOLAR_TO_GRID
            ),
            BatteryToHouse(
                coordinator, config_entry, entity_description=_BATTERY_TO_HOUSE
            ),
            BatteryToGrid(
                coordinator, config_entry, entity_description=_BATTERY_TO_GRID
            ),
            GridToHouse(
                coordinator, config_entry, entity_description=_GRID_TO_HOUSE
            ),
            GridToBattery(
                coordinator, config_entry, entity_description=_GRID_TO_BATTERY
            ),
        ]
    )

    # Add battery sensors
    for batt_num, batt in enumerate(coordinator.data.batteries):
        # Only add data for batteries if we can successfully read the serial number
        # Failure to read a S/N can result in null bytes
        if batt.battery_serial_number.replace("\x00", ""):
            entities.extend(
                [
                    BatteryBasicSensor(
                        coordinator, config_entry, entity_description, batt_num
                    )
                    for entity_description in _BASIC_BATTERY_SENSORS
                ]
            )

            entities.extend(
                [
                    BatteryRemainingCapacitySensor(
                        coordinator,
                        config_entry,
                        entity_description=_BATTERY_REMAINING_CAPACITY_SENSOR,
                        battery_id=batt_num,
                    ),
                    BatteryCellsVoltageSensor(
                        coordinator,
                        config_entry,
                        entity_description=_BATTERY_CELLS_VOLTAGE_SENSOR,
                        battery_id=batt_num,
                    ),
                ]
            )
        else:
            LOGGER.warning("Ignoring battery %d due to missing serial number", batt_num)

    async_add_entities(entities)


class InverterBasicSensor(InverterEntity, SensorEntity):
    """A sensor that derives its value from the register values fetched from the inverter."""

    def __init__(
        self,
        coordinator: GivEnergyUpdateCoordinator,
        config_entry: ConfigEntry,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize a sensor based on an entity description."""
        super().__init__(coordinator, config_entry)
        self._attr_unique_id = (
            f"{self.data.inverter_serial_number}_{entity_description.key}"
        )
        self.entity_description = entity_description

    @property
    def native_value(self) -> StateType:
        """Return the register value as referenced by the 'key' property of the associated entity description."""
        return self.data.dict().get(self.entity_description.key)


class PVEnergyTodaySensor(InverterBasicSensor):
    """Total PV Energy sensor."""

    @property
    def native_value(self) -> StateType:
        """Return the sum of energy generated across both PV strings."""
        return self.data.e_pv1_day + self.data.e_pv2_day


class PVPowerSensor(InverterBasicSensor):
    """Total PV Power sensor."""

    @property
    def native_value(self) -> StateType:
        """Return the sum of power generated across both PV strings."""
        return self.data.p_pv1 + self.data.p_pv2


class ConsumptionTodaySensor(InverterBasicSensor):
    """Consumption Today sensor."""

    @property
    def native_value(self) -> StateType:
        """Calculate consumption based on net inverter output plus net grid import."""

        consumption_today = (
            self.data.e_inverter_out_day
            - self.data.e_inverter_in_day
            + self.data.e_grid_in_day
            - self.data.e_grid_out_day
        )

        # For AC inverters, PV output doesn't count as part of the inverter output,
        # so we need to add it on.
        if self.data.inverter_model == Model.AC:
            consumption_today += self.data.e_pv1_day + self.data.e_pv2_day

        return consumption_today


class ConsumptionTotalSensor(InverterBasicSensor):
    """Consumption Total sensor."""

    @property
    def native_value(self) -> StateType:
        """Calculate consumption based on net inverter output plus net grid import."""
        consumption_total = (
            self.data.e_inverter_out_total
            - self.data.e_inverter_in_total
            + self.data.e_grid_in_total
            - self.data.e_grid_out_total
        )

        # For AC inverters, PV output doesn't count as part of the inverter output,
        # so we need to add it on.
        if self.data.inverter_model == Model.AC:
            consumption_total += self.data.e_pv_total

        return consumption_total


class GridImportPower(InverterBasicSensor):
    """Grid Import Power (absolute value derived from Grid Power if importing)"""

    @property
    def native_value(self) -> StateType:
        grid_import_power = 0
        """Or grid_import_power has a value if we're importing"""
        if self.data.p_grid_out < 0:
            grid_import_power = abs(self.data.p_grid_out)
        return grid_import_power
    
class GridExportPower(InverterBasicSensor):
    """Grid Export Power (absolute value derived from Grid Power if exporting)"""

    @property
    def native_value(self) -> StateType:
        grid_export_power = 0
        """Or grid_export_power has a value if we're exporting"""
        if self.data.p_grid_out > 0:
            grid_export_power = abs(self.data.p_grid_out)
        return grid_export_power

class BatteryModeSensor(InverterBasicSensor):
    """Battery mode sensor."""

    @property
    def native_value(self) -> StateType:
        """Determine the mode based on various settings."""

        # battery_power_mode:
        # 0: export/max
        # 1: demand/self-consumption
        battery_power_mode = self.data.battery_power_mode
        enable_discharge = self.data.enable_discharge

        if battery_power_mode == 1 and enable_discharge is False:
            return "Eco"

        if enable_discharge is True:
            if battery_power_mode == 1:
                return "Timed Discharge"
            else:
                return "Timed Export"
        return "Unknown"


class BatteryBasicSensor(BatteryEntity, SensorEntity):
    """
    A battery sensor that derives its value from the register values fetched from the inverter.

    Values are as reported from the BMS in each battery. Sometimes there are differences in
    values as reported by the inverter itself and the BMS.
    """

    def __init__(
        self,
        coordinator: GivEnergyUpdateCoordinator,
        config_entry: ConfigEntry,
        entity_description: SensorEntityDescription,
        battery_id: int,
    ) -> None:
        """Initialize a sensor based on an entity description."""
        super().__init__(coordinator, config_entry, battery_id)
        self._attr_unique_id = (
            f"{self.data.battery_serial_number}_{entity_description.key}"
        )
        self.entity_description = entity_description

    @property
    def native_value(self) -> StateType:
        """Get the register value whose name matches the entity key."""
        return self.data.dict().get(self.entity_description.key)


class BatteryRemainingCapacitySensor(BatteryBasicSensor):
    """Battery remaining capacity sensor."""

    @property
    def native_value(self) -> StateType:
        """Map the low-level Ah value to energy in kWh."""
        battery_remaining_capacity = (
            self.data.battery_remaining_capacity * self.data.v_battery_cells_sum / 1000
        )
        # Raw value is in Ah (Amp Hour)
        # Convert to KWh using formula Ah * V / 1000
        return round(battery_remaining_capacity, 3)


class BatteryCellsVoltageSensor(BatteryBasicSensor):
    """Battery cell voltage sensor."""

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Expose individual cell voltages."""
        num_cells = self.data.battery_num_cells
        return self.data.dict(  # type: ignore[no-any-return]
            include={f"v_battery_cell_{i:02d}" for i in range(1, num_cells + 1)}
        )
    
    # POWER FLOW STATS
    
    # SOLAR TO HOUSE / BATTERY / GRID
class SolarToHouse(InverterBasicSensor):
    """Solar to house derivation"""

    @property
    def native_value(self) -> StateType:
        PV_power = self.data.p_pv1 + self.data.p_pv2
        if PV_power <= 0:
            return 0
        """min(PV_power, load_power)"""
        ##!! with p_load_demand there's a section in givtcp about being <15500 - not really sure what that's for
        S2H = min((self.data.p_pv1 + self.data.p_pv2),self.data.p_load_demand)
        return S2H
    
class SolarToBattery(InverterBasicSensor):
    """Solar to battery derivation"""

    @property
    def native_value(self) -> StateType:
        PV_power = self.data.p_pv1 + self.data.p_pv2
        if PV_power <= 0:
            return 0
        """max((PV_power-S2H)-export_power,0)"""
        S2H = min((self.data.p_pv1 + self.data.p_pv2),self.data.p_load_demand)
        grid_export_power = 0
        if self.data.p_grid_out > 0:
            grid_export_power = abs(self.data.p_grid_out)
        S2B = max((PV_power-S2H)-grid_export_power,0)
        return S2B

class SolarToGrid(InverterBasicSensor):
    """Solar to Grid derivation"""

    @property
    def native_value(self) -> StateType:
        PV_power = self.data.p_pv1 + self.data.p_pv2
        if PV_power <= 0:
            return 0
        """max(PV_power - S2H - S2B,0)"""
        S2H = min((self.data.p_pv1 + self.data.p_pv2),self.data.p_load_demand)
        grid_export_power = 0
        if self.data.p_grid_out > 0:
            grid_export_power = abs(self.data.p_grid_out)
        S2B = max((PV_power - S2H) - grid_export_power,0)
        S2G = max(PV_power - S2H - S2B,0)
        return S2G
    
    #Battery to House
class BatteryToHouse(InverterBasicSensor):
    """Battery to house derivation"""

    @property
    def native_value(self) -> StateType:
        """max(discharge_power-export_power,0)"""
        discharge_power = 0
        battery_power = self.data.p_battery
        if battery_power >= 0:
            discharge_power = abs(battery_power)
        grid_export_power = 0
        if self.data.p_grid_out > 0:
            grid_export_power = abs(self.data.p_grid_out)
        B2H = max(discharge_power - grid_export_power, 0)
        return B2H
    
    #Battery to Grid
class BatteryToGrid(InverterBasicSensor):
    """Battery to Grid derivation"""

    @property
    def native_value(self) -> StateType:
        """max(discharge_power-B2H,0) unless grid export power = 0"""
        B2G = 0
        grid_export_power = 0
        if self.data.p_grid_out > 0:
            grid_export_power = abs(self.data.p_grid_out)
        if grid_export_power = 0:
            return B2G
        discharge_power = 0
        battery_power = self.data.p_battery
        if battery_power >= 0:
            discharge_power = abs(battery_power)
        grid_export_power = 0
        if self.data.p_grid_out > 0:
            grid_export_power = abs(self.data.p_grid_out)
        B2H = max(discharge_power - grid_export_power, 0)
        B2G = max(discharge_power - B2H, 0)
        return B2G
        
    #Grid to Battery
class GridToBattery(InverterBasicSensor):
    """Grid to Battery derivation"""

    @property
    def native_value(self) -> StateType:
        """charge_power-max(PV_power-Load_power,0) unless grid import power > 0"""
        G2B = 0
        grid_import_power = 0
        if self.data.p_grid_out < 0:
            grid_import_power = abs(self.data.p_grid_out)
        if grid_import_power > 0:
            return G2B
        PV_power = self.data.p_pv1 + self.data.p_pv2
        load_power = self.data.p_load_demand
        charge_power = 0
        battery_power = self.data.p_battery
        if battery_power > 0:
            charge_power = abs(battery_power)
        G2B = charge_power - max(PV_power-load_power,0)
        return G2B
 
    #Grid to House
class GridToHouse(InverterBasicSensor):
    """Grid to house derivation"""

    @property
    def native_value(self) -> StateType:
        """charge_power-max(PV_power-Load_power,0) unless grid import power > 0"""
        G2H = 0
        grid_import_power = 0
        if self.data.p_grid_out < 0:
            grid_import_power = abs(self.data.p_grid_out)
        if grid_import_power > 0:
            return G2H
        charge_power = 0
        battery_power = self.data.p_battery
        if battery_power > 0:
            charge_power = abs(battery_power)
        G2H = max(grid_import_power-charge_power,0)
        return G2H
