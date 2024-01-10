import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, voltage_sampler
from esphome.const import (
    CONF_ID,
    CONF_PIN,
    CONF_RAW,
    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    UNIT_VOLT,
)

from . import (
    CONF_ARDUINO_PORT_EXPANDER_ID,
    ArduinoPortExpanderComponent,
    arduino_port_expander_ns,
)

ANALOG_PIN = {
    "A0": 0,
    "A1": 1,
    "A2": 2,
    "A3": 3,
    "A6": 6,
    "A7": 7,
}

AUTO_LOAD = ["voltage_sampler"]


ArduinoPortExpanderSensor = arduino_port_expander_ns.class_(
    "ArduinoPortExpanderSensor",
    sensor.Sensor,
    cg.PollingComponent,
    voltage_sampler.VoltageSampler,
)

CONFIG_SCHEMA = cv.All(
    sensor.sensor_schema(
        ArduinoPortExpanderSensor,
        unit_of_measurement=UNIT_VOLT,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    )
    .extend(
        {
            cv.GenerateID(): cv.declare_id(ArduinoPortExpanderSensor),
            cv.GenerateID(CONF_ARDUINO_PORT_EXPANDER_ID): cv.use_id(
                ArduinoPortExpanderComponent
            ),
            cv.Required(CONF_PIN): cv.enum(ANALOG_PIN),
            cv.Optional(CONF_RAW, default="false"): cv.boolean,
        }
    )
    .extend(cv.polling_component_schema("60s")),
)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_ARDUINO_PORT_EXPANDER_ID])

    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)

    cg.add(var.set_pin(config[CONF_PIN]))
    cg.add(var.set_raw(config[CONF_RAW]))
    cg.add(var.set_parent(hub))
