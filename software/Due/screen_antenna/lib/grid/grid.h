//
// Created by n7 on 2/6/23.
//

#ifndef SCREEN_ANTENNA_GRID_H
#define SCREEN_ANTENNA_GRID_H

#include <cstdint>
#include <vector>

#include "ad_conv.h"
#include "led_drv.h"
#include "rgb_led.h"

class Grid {
    std::vector<std::vector<RGBLED>> rgb_leds;
    std::vector<LEDDrv> led_drvs;
    std::vector<ADConv> ad_convs;

public:
    Grid(uint8_t n_rgb_leds_rows, uint8_t n_rgb_leds_cols,
         uint8_t n_led_drvs, uint8_t n_ad_convs):
            rgb_leds(n_rgb_leds_rows ,
                     std::vector<RGBLED> (n_rgb_leds_cols,
                                          RGBLED())),
            led_drvs(n_led_drvs, LEDDrv()),
            ad_convs(n_ad_convs, ADConv()) {};

    void begin(uint32_t uart_baud_rate, uint32_t i2c_freq_hz,
               uint32_t spi_freq_hz);

    void assignLEDDrvAddr(uint8_t led_drv_id, uint8_t led_drv_addr);
    void assignADConvShdnPin(uint8_t ad_conv_id, uint8_t ad_conv_shdn_pin);
    void assignADConvFreqHz(uint8_t ad_conv_id, uint32_t ad_conv_freq_hz);
    void beginADConv(uint8_t ad_conv_id);

    void connectRGBLEDToLEDDrv(uint8_t rgb_led_row, uint8_t rgb_led_col,
                               uint8_t led_drv_id, uint8_t led_drv_ch_r,
                               uint8_t led_drv_ch_g, uint8_t led_drv_ch_b);
    void connectRGBLEDToADConv(uint8_t rgb_led_row, uint8_t rgb_led_col,
                               uint8_t ad_conv_id, uint8_t ad_conv_ch_r);

    void setPWMR(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val);
    void setPWMG(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val);
    void setPWMB(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val);
    void setPWM3(uint8_t rgb_led_row, uint8_t rgb_led_col,
                 uint8_t r_val, uint8_t g_val, uint8_t b_val);
    void setPWM3(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val);
    void setPWMRAll(uint8_t val);
    void setPWMGAll(uint8_t val);
    void setPWMBAll(uint8_t val);
    void setPWM3All(uint8_t r_val, uint8_t g_val, uint8_t b_val);
    void setPWM3All(uint8_t val);

    void setIR(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val);
    void setIG(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val);
    void setIB(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val);
    void setI3(uint8_t rgb_led_row, uint8_t rgb_led_col,
               uint8_t r_val, uint8_t g_val, uint8_t b_val);
    void setI3(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val);
    void setIRAll(uint8_t val);
    void setIGAll(uint8_t val);
    void setIBAll(uint8_t val);
    void setI3All(uint8_t r_val, uint8_t g_val, uint8_t b_val);
    void setI3All(uint8_t val);

    uint16_t getV(uint8_t rgb_led_row, uint8_t rgb_led_col);
    uint8_t get_n_rows() const;
    uint8_t get_n_cols() const;
    uint8_t get_n_drvs() const;
    uint8_t get_n_adcs() const;
};

#endif //SCREEN_ANTENNA_GRID_H
