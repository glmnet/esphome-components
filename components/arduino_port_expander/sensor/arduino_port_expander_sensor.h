#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/voltage_sampler/voltage_sampler.h"
#include "../arduino_port_expander.h"

namespace esphome {
namespace arduino_port_expander {

class ArduinoPortExpanderSensor : public PollingComponent,
                                  public sensor::Sensor,
                                  public voltage_sampler::VoltageSampler {
 public:
  void set_parent(ArduinoPortExpanderComponent *parent) { this->parent_ = parent; }

  void set_pin(uint8_t pin) { this->pin_ = pin; };
  void set_raw(bool raw) { this->raw_ = raw; };

  void update() override;

  float sample() override;

 protected:
  uint8_t pin_;
  bool raw_;
  ArduinoPortExpanderComponent *parent_;
};
}  // namespace arduino_port_expander
}  // namespace esphome