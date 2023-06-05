//
// Created by n7 on 8/12/22.
//

#include "rgb_led.h"

void RGBLED::connectLEDDrv(LEDDrv *drv, uint8_t drv_ch_r, uint8_t drv_ch_g,
                           uint8_t drv_ch_b) {
    drv_ = drv;
    drv_ch_r_ = drv_ch_r;
    drv_ch_g_ = drv_ch_g;
    drv_ch_b_ = drv_ch_b;
}

void RGBLED::connectADConv(ADConv *adc, uint8_t adc_ch_r) {
    adc_ = adc;
    adc_ch_r_ = adc_ch_r;
}

void RGBLED::setPWMR(uint8_t val) {
    drv_->setLEDPWM(drv_ch_r_, val);
}

void RGBLED::setPWMG(uint8_t val) {
    drv_->setLEDPWM(drv_ch_g_, val);
}

void RGBLED::setPWMB(uint8_t val) {
    drv_->setLEDPWM(drv_ch_b_, val);
}

void RGBLED::setPWM3(uint8_t r_val, uint8_t g_val, uint8_t b_val) {
    setPWMR(r_val);
    setPWMG(g_val);
    setPWMB(b_val);
}

void RGBLED::setPWM3(uint8_t val) {
    setPWMR(val);
    setPWMG(val);
    setPWMB(val);
}

void RGBLED::setIR(uint8_t val) {
    drv_->setLEDI(drv_ch_r_, val);
}

void RGBLED::setIG(uint8_t val) {
    drv_->setLEDI(drv_ch_g_, val);
}

void RGBLED::setIB(uint8_t val) {
    drv_->setLEDI(drv_ch_b_, val);
}

void RGBLED::setI3(uint8_t r_val, uint8_t g_val, uint8_t b_val) {
    setIR(r_val);
    setIG(g_val);
    setIB(b_val);
}

void RGBLED::setI3(uint8_t val) {
    setIR(val);
    setIG(val);
    setIB(val);
}

uint16_t RGBLED::getV() {
    return adc_->readChan(adc_ch_r_);
}
