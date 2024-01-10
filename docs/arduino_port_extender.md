# Arduino Port Expander

With this sketch you can control pins of a remote Arduino board through
ESPHome. The Arduino acts as a port expander, allowing you to use more
pins than a standard ESP8266/ESP32 has.

![Local Image](images/arduino_pro_mini.jpg)

The Arduino is connected to the ESP via I²C. Most Arduinos use the `A4`
and `A5` pins for the I²C bus so those pins are not available to read
from ESPHome. It is recommended to use a 3.3V I/O level Arduino, however
using 5V Arduinos seems to work too. In the latter case you should power
your 5V Arduino with 3.3V otherwise you will need a level converter for
the I²C bus.

Currently it is supported:

> - reading digital inputs
> - reading analog inputs
> - writing digital outputs

The Arduino sketch can be retrieved from
[here](https://gist.github.com/glmnet/49ca3d6a9742fc3649f4fbdeaa4cdf5d#file-arduino_port_expander_sketch-ino)
you can rename it to `.ino` and use the Arduino IDE to program it.

To setup the [external component](https://esphome.io/components/external_components) add the external component definition to your
yaml:

```yaml
external_components:
  source: github://glmnet/esphome-components
  components: [arduino_port_expander]
```

Setup your [I²C Bus](https://esphome.io/components/i2c):

```yaml
i2c:
```

By default ESP8266 uses `SDA` pin `GPIO4` which you need to connect to
Arduino\'s `A4` and the `SCL` is `GPIO5` which goes to Arduino\'s `A5`.

Then create a `arduino_port_expander` component hub, this will be the main component we will be referencing later when creating individual IOs.

```yaml
arduino_port_expander:
  id: ape1 # must identify somehow to later use
  address: 0x08
  analog_reference: DEFAULT
```

By default the I²C `address` is `0x08` but you can change it on the
Arduino sketch so you can have more devices on the same bus.

`analog_reference` can be `DEFAULT` or `INTERNAL`. Default is `INTERNAL`. See
Arduino [analogReference()](https://www.arduino.cc/reference/en/language/functions/analog-io/analogreference/) function for details.

`reference_voltage` is the maximum value that can be measured.
If the `analog_reference` is `DEFAULT`, then this should be the voltage that your Arduino board runs at, either `5` (default) or `3.3`.
If the `analog_reference` is `INTERNAL`, then this will be `1.1` (default) or `2.56`.  See the `analogReference()` link for details.

## `gpio` pins

Use pins as any other port expander in ESPHome, you can use it in almost every place a pin is needed:

```yaml
binary_sensor:
  - platform: gpio
    pin:
      arduino_port_expander: ape1
      number: 2
      mode:
        input: true # defaults to False
        output: false # defaults to False
        pullup: true # defaults to False
```

You can use any PIN from 0 to 13 or `A0` to `A3` (`A4` and `A5` are used for
I²C and `A6` and `A7` do not support internal pull up).
For A0 use 14, A1, 15 and so on.

Note: Arduino PIN 13 usually has a LED connected to it and using it as digital
input with the built in internal pull up might be problematic, using it
as an output is preferred.

## Sensor

Sensors allows for reading the analog value of an analog pin, those are
from `A0` to `A7` except for `A4` and `A5` which are used for the i2c connection.

Arduino analog inputs measures voltage. By default the sketch is
configured to use the Arduino internal VREF reference setup to 1.1 volt, so
higher voltages are read as 1023. You can configure Arduino to compare
the voltage to VIN voltage, this voltage might be 5 volts or 3.3 volts,
depending on how you are powering it.  See the main component config to declare
which voltage your board uses.

`raw: true` will return the raw measured value from 0-1023 (the value returned by the Arduino `analogRead` function) instead of the calculated voltage.

```yaml
sensor:
  - platform: arduino_port_expander
    id: sx
    pin: A0
    name: Ardu A0
    update_interval: 10s
```
