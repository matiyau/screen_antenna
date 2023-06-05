//
// Created by n7 on 8/12/22.
//

#ifndef SCREEN_ANTENNA_RGB_LED_H
#define SCREEN_ANTENNA_RGB_LED_H

#include <cstdint>

#include "../led_drv/led_drv.h"
#include "../ad_conv/ad_conv.h"


class RGBLED {
    LEDDrv *drv_;
    uint8_t drv_ch_r_;
    uint8_t drv_ch_g_;
    uint8_t drv_ch_b_;

    ADConv *adc_;
    uint8_t adc_ch_r_;

public:
    RGBLED() {};

    RGBLED(LEDDrv *drv, uint8_t drv_ch_r, uint8_t drv_ch_g,
           uint8_t drv_ch_b, ADConv *adc, uint8_t adc_ch_r)
           : drv_(drv), drv_ch_r_(drv_ch_r), drv_ch_g_(drv_ch_g),
           drv_ch_b_(drv_ch_b), adc_(adc), adc_ch_r_(adc_ch_r)
           {};

    void connectLEDDrv(LEDDrv *drv, uint8_t drv_ch_r, uint8_t drv_ch_g,
                       uint8_t drv_ch_b);

    void connectADConv(ADConv *ad_conv, uint8_t ad_conv_ch_r);

    void setPWMR(uint8_t val);
    void setPWMG(uint8_t val);
    void setPWMB(uint8_t val);
    void setPWM3(uint8_t r_val, uint8_t g_val, uint8_t b_val);
    void setPWM3(uint8_t val);

    void setIR(uint8_t val);
    void setIG(uint8_t val);
    void setIB(uint8_t val);
    void setI3(uint8_t r_val, uint8_t g_val, uint8_t b_val);
    void setI3(uint8_t val);

    uint16_t getV();
};


#endif //SCREEN_ANTENNA_RGB_LED_H
