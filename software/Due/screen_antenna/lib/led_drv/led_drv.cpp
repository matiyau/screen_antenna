//
// Created by n7 on 8/12/22.
//

#include <Wire.h>

#include "led_drv.h"

void LEDDrv::assignAddr(uint8_t addr) {
    addr_ = addr;
}

void LEDDrv::setLEDPWM(uint8_t chan, uint8_t val) {
    setRegister(REG_PWM_LED_0 + chan, val);
}

void LEDDrv::setLEDPWMAll(uint8_t val) {
    setRegister(REG_PWM_LED_ALL, val);
}

void LEDDrv::setLEDI(uint8_t chan, uint8_t val) {
    setRegister(REG_I_LED_0 + chan, val);
}

void LEDDrv::setLEDIAll(uint8_t val) {
    setRegister(REG_I_LED_ALL, val);
}

void LEDDrv::setLEDGrpPWM(uint8_t val) {
    setRegister(REG_GRP_PWM, val);
}

void LEDDrv::setLEDGrpFreq(uint8_t val) {
    setRegister(REG_GRP_FREQ, val);
}

void LEDDrv::setRegister(uint8_t num, uint8_t val) {
    Wire.beginTransmission(addr_);
    Wire.write(num);
    Wire.write(val);
    Wire.endTransmission();
}