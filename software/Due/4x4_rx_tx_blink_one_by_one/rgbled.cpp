#include "rgbled.h"

void RGBLED::setPWMR(uint8_t val) {
  if (val != pwm_r_val) {
    drv.pwmLED(drv_ch_r, val);
    pwm_r_val = val;
  }
}

void RGBLED::setPWMG(uint8_t val) {
  if (val != pwm_g_val) {
    drv.pwmLED(drv_ch_g, val);
    pwm_g_val = val;
  }
}

void RGBLED::setPWMB(uint8_t val) {
  if (val != pwm_b_val) {
    drv.pwmLED(drv_ch_b, val);
    pwm_b_val = val;
  }
}

void RGBLED::setPWM(uint8_t r_val, uint8_t g_val, uint8_t b_val) {
  setPWMR(r_val);
  setPWMG(g_val);
  setPWMB(b_val);
}

void RGBLED::setPWM(uint8_t val) {
  setPWMR(val);
  setPWMG(val);
  setPWMB(val);
}

void RGBLED::setIR(uint8_t val) {
  if (val != i_r_val) {
    drv.setLEDCurrent(drv_ch_r, val);
    i_r_val = val;
  }
}

void RGBLED::setIG(uint8_t val) {
  if (val != i_g_val) {
    drv.setLEDCurrent(drv_ch_g, val);
    i_g_val = val;
  }
}

void RGBLED::setIB(uint8_t val) {
  if (val != i_b_val) {
    drv.setLEDCurrent(drv_ch_b, val);
    i_b_val = val;
  }
}

void RGBLED::setI(uint8_t r_val, uint8_t g_val, uint8_t b_val) {
  setIR(r_val);
  setIG(g_val);
  setIB(b_val);
}

void RGBLED::setI(uint8_t val) {
  setIR(val);
  setIG(val);
  setIB(val);
}

int16_t RGBLED::getADCR() {
  return adc.readADC(adc_ch_r);
}
