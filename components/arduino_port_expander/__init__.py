import esphome.codegen as cg
import esphome.config_validation as cv
from voluptuous import NotIn
from esphome import pins
from esphome.components import i2c
from esphome.const import (
    CONF_ID,
    CONF_INPUT,
    CONF_NUMBER,
    CONF_MODE,
    CONF_INVERTED,
    CONF_OUTPUT,
    CONF_PULLUP,
)

CONF_ARDUINO_PORT_EXPANDER = "arduino_port_expander"
CONF_ARDUINO_PORT_EXPANDER_ID = "arduino_port_expander_id"
CONF_ANALOG_REFERENCE = "analog_reference"

DEPENDENCIES = ["i2c"]
MULTI_CONF = True

arduino_port_expander_ns = cg.esphome_ns.namespace("arduino_port_expander")

ArduinoPortExpanderAnalogReference = arduino_port_expander_ns.enum(
    "ArduinoPortExpanderAnalogReference"
)
ANALOG_REFERENCE = {
    "INTERNAL": ArduinoPortExpanderAnalogReference.ANALOG_REFERENCE_INTERNAL,
    "DEFAULT": ArduinoPortExpanderAnalogReference.ANALOG_REFERENCE_DEFAULT,
}

ArduinoPortExpanderComponent = arduino_port_expander_ns.class_(
    "ArduinoPortExpanderComponent", cg.Component, i2c.I2CDevice
)
ArduinoPortExpanderGPIOPin = arduino_port_expander_ns.class_(
    "ArduinoPortExpanderGPIOPin", cg.GPIOPin
)

CONF_ArduinoPortExpander = "arduino_port_expander"

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.declare_id(ArduinoPortExpanderComponent),
            cv.Optional(CONF_ANALOG_REFERENCE, default="INTERNAL"): cv.enum(
                ANALOG_REFERENCE
            ),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(i2c.i2c_device_schema(0x08))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)
    cg.add(var.set_analog_refernce(config[CONF_ANALOG_REFERENCE]))


def validate_mode(value):
    if not (value[CONF_INPUT] or value[CONF_OUTPUT]):
        raise cv.Invalid("Mode must be either input or output")
    if value[CONF_INPUT] and value[CONF_OUTPUT]:
        raise cv.Invalid("Mode must be either input or output")
    return value


ARDUINO_PORT_EXPANDER_PIN_SCHEMA = cv.All(
    {
        cv.GenerateID(): cv.declare_id(ArduinoPortExpanderGPIOPin),
        cv.Required(CONF_ArduinoPortExpander): cv.use_id(ArduinoPortExpanderComponent),
        cv.Required(CONF_NUMBER): cv.All(
            cv.int_range(min=0, max=21),
            NotIn([18], "A4 is used for I2C SDA"),
            NotIn([19], "A5 is used for I2C SCL"),
        ),
        cv.Optional(CONF_MODE, default={}): cv.All(
            {
                cv.Optional(CONF_INPUT, default=False): cv.boolean,
                cv.Optional(CONF_OUTPUT, default=False): cv.boolean,
                cv.Optional(CONF_PULLUP, default=False): cv.boolean,
            },
            validate_mode,
        ),
        cv.Optional(CONF_INVERTED, default=False): cv.boolean,
    }
)


@pins.PIN_SCHEMA_REGISTRY.register(
    CONF_ARDUINO_PORT_EXPANDER, ARDUINO_PORT_EXPANDER_PIN_SCHEMA
)
async def ArduinoPortExpander_pin_to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    parent = await cg.get_variable(config[CONF_ARDUINO_PORT_EXPANDER])

    cg.add(var.set_parent(parent))

    num = config[CONF_NUMBER]
    cg.add(var.set_pin(num))
    cg.add(var.set_inverted(config[CONF_INVERTED]))
    cg.add(var.set_flags(pins.gpio_flags_expr(config[CONF_MODE])))
    return var
