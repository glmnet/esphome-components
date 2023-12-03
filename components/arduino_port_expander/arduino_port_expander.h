#pragma once

#include "esphome/core/component.h"
#include "esphome/core/hal.h"
#include "esphome/components/i2c/i2c.h"
#include "esphome/core/defines.h"
#ifdef USE_SENSOR
#include "esphome/components/sensor/sensor.h"
#endif

namespace esphome {
namespace arduino_port_expander {

enum ArduinoPortExpanderAnalogReference : uint8_t {
  ANALOG_REFERENCE_INTERNAL = 0x10,
  ANALOG_REFERENCE_DEFAULT = 0x11,
};

class ArduinoPortExpanderComponent : public Component, public i2c::I2CDevice {
 public:
  ArduinoPortExpanderComponent() = default;

  void setup() override;
  /// Poll i2c
  void loop() override;
  /// Helper function to read the value of a pin.
  bool digital_read(uint8_t pin);
  /// Helper function to write the value of a pin.
  void digital_write(uint8_t pin, bool value);
  /// Helper function to read the voltage of a pin.
  float analog_read(uint8_t pin);
  /// Helper function to set the pin mode of a pin.
  void pin_mode(uint8_t pin, gpio::Flags flags);

  float get_setup_priority() const override;
  void set_analog_refernce(ArduinoPortExpanderAnalogReference analog_reference) {
    analog_reference_ = analog_reference;
  }
  ArduinoPortExpanderAnalogReference get_analog_reference() { return analog_reference_; }

  void dump_config() override;

 protected:
  void setup_();
  void poll_();
  bool read_gpio_();

  bool write_gpio_();

  uint8_t read_buffer_[3]{0, 0, 0};
  bool read_valid_{false};
  ArduinoPortExpanderAnalogReference analog_reference_;
};

/// Helper class to expose a ArduinoPortExpander pin as an internal input GPIO pin.
class ArduinoPortExpanderGPIOPin : public GPIOPin {
 public:
  void setup() override;
  void pin_mode(gpio::Flags flags) override;

  bool digital_read() override;
  void digital_write(bool value) override;
  std::string dump_summary() const override;

  void set_parent(ArduinoPortExpanderComponent *parent) { parent_ = parent; }
  void set_pin(uint8_t pin) { pin_ = pin; }
  void set_inverted(bool inverted) { inverted_ = inverted; }
  void set_flags(gpio::Flags flags) { flags_ = flags; }

 protected:
  ArduinoPortExpanderComponent *parent_;
  uint8_t pin_;
  bool inverted_;
  bool setup_;
  gpio::Flags flags_;
};

#ifdef USE_SENSOR
class ArduinoPortExpanderSensor : public PollingComponent, public sensor::Sensor {
 public:
  void set_parent(ArduinoPortExpanderComponent *parent) { parent_ = parent; }
  /// Helper to get a pointer to the address as uint8_t.

  void set_pin(uint8_t pin) { pin_ = pin; };

  void update() override;

 protected:
  uint8_t pin_;
  ArduinoPortExpanderComponent *parent_;
};

#endif

}  // namespace arduino_port_expander
}  // namespace esphome
