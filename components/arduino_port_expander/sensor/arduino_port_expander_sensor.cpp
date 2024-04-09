#include "arduino_port_expander_sensor.h"

namespace esphome {
namespace arduino_port_expander {

float ArduinoPortExpanderSensor::sample() {
  auto value = this->parent_->analog_read(this->pin_);

  if (this->raw_)
    return value;

  value = value / 1023.0 * this->parent_->get_reference_voltage();
  return value;
}

void ArduinoPortExpanderSensor::update() { this->publish_state(this->sample()); }

}  // namespace arduino_port_expander
}  // namespace esphome