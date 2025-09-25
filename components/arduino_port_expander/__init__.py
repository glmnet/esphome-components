ARDUINO_PORT_EXPANDER_PIN_SCHEMA = cv.All(
    {
        cv.GenerateID(): cv.declare_id(ArduinoPortExpanderGPIOPin),
        cv.Required(CONF_ArduinoPortExpander): cv.use_id(ArduinoPortExpanderComponent),
        cv.Required(CONF_NUMBER): cv.All(
            cv.int_range(min=0, max=69),  # Mega soporta 0–69 (D0–D53, A0–A15)
            NotIn([20], "Pin 20 (SDA) está reservado para I2C"),
            NotIn([21], "Pin 21 (SCL) está reservado para I2C"),
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
