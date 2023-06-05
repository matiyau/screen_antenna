//
// Created by n7 on 2/6/23.
//

#include <Wire.h>
#undef max
#undef min

#include "grid.h"

void Grid::begin(uint32_t uart_baud_rate, uint32_t i2c_freq_hz,
                 uint32_t spi_freq_hz) {

    Serial.begin(uart_baud_rate);
    while(!Serial);

    Wire.begin();
    Wire.setClock(i2c_freq_hz);

    for (uint8_t i=0; i<ad_convs.size(); i++) {
        assignADConvFreqHz(i, spi_freq_hz);
        beginADConv(i);
    }
}

void Grid::assignLEDDrvAddr(uint8_t led_drv_id, uint8_t led_drv_addr) {
    led_drvs[led_drv_id].assignAddr(led_drv_addr);
}

void Grid::assignADConvShdnPin(uint8_t ad_conv_id, uint8_t ad_conv_shdn_pin) {
    ad_convs[ad_conv_id].assignShdnPin(ad_conv_shdn_pin);
}

void Grid::assignADConvFreqHz(uint8_t ad_conv_id, uint32_t ad_conv_freq_hz) {
    ad_convs[ad_conv_id].assignFreqHz(ad_conv_freq_hz);
}

void Grid::beginADConv(uint8_t ad_conv_id) {
    ad_convs[ad_conv_id].begin();
}

void Grid::connectRGBLEDToLEDDrv(uint8_t rgb_led_row, uint8_t rgb_led_col,
                                 uint8_t led_drv_id, uint8_t led_drv_ch_r,
                                 uint8_t led_drv_ch_g,
                                 uint8_t led_drv_ch_b) {
    rgb_leds[rgb_led_row][rgb_led_col].connectLEDDrv(&(led_drvs[led_drv_id]),
                                                     led_drv_ch_r,
                                                     led_drv_ch_g,
                                                     led_drv_ch_b);
}

void Grid::connectRGBLEDToADConv(uint8_t rgb_led_row, uint8_t rgb_led_col,
                                 uint8_t ad_conv_id, uint8_t ad_conv_ch_r) {
    rgb_leds[rgb_led_row][rgb_led_col].connectADConv(&(ad_convs[ad_conv_id]),
                                                     ad_conv_ch_r);
}

void Grid::setPWMR(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val) {
    rgb_leds[rgb_led_row][rgb_led_col].setPWMR(val);
}

void Grid::setPWMG(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val) {
    rgb_leds[rgb_led_row][rgb_led_col].setPWMG(val);
}

void Grid::setPWMB(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val) {
    rgb_leds[rgb_led_row][rgb_led_col].setPWMB(val);
}

void Grid::setPWM3(uint8_t rgb_led_row, uint8_t rgb_led_col,
                   uint8_t r_val, uint8_t g_val, uint8_t b_val) {
    rgb_leds[rgb_led_row][rgb_led_col].setPWM3(r_val, g_val, b_val);
}

void Grid::setPWM3(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val) {
    rgb_leds[rgb_led_row][rgb_led_col].setPWM3(val);
}

void Grid::setPWMRAll(uint8_t val) {
    for (uint8_t i=0; i<rgb_leds.size(); i++) {
        for (uint8_t j=0; j<rgb_leds[0].size(); j++) {
            rgb_leds[i][j].setPWMR(val);
        }
    }
}

void Grid::setPWMGAll(uint8_t val) {
    for (uint8_t i=0; i<rgb_leds.size(); i++) {
        for (uint8_t j=0; j<rgb_leds[0].size(); j++) {
            rgb_leds[i][j].setPWMG(val);
        }
    }
}

void Grid::setPWMBAll(uint8_t val) {
    for (uint8_t i=0; i<rgb_leds.size(); i++) {
        for (uint8_t j=0; j<rgb_leds[0].size(); j++) {
            rgb_leds[i][j].setPWMB(val);
        }
    }
}

void Grid::setPWM3All(uint8_t r_val, uint8_t g_val, uint8_t b_val) {
    for (uint8_t i=0; i<rgb_leds.size(); i++) {
        for (uint8_t j=0; j<rgb_leds[0].size(); j++) {
            rgb_leds[i][j].setPWM3(r_val, g_val, b_val);
        }
    }
}

void Grid::setPWM3All(uint8_t val) {
    for (uint8_t i=0; i<led_drvs.size(); i++) {
        led_drvs[i].setLEDPWMAll(val);
    }
}


void Grid::setIR(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val) {
    rgb_leds[rgb_led_row][rgb_led_col].setIR(val);
}

void Grid::setIG(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val) {
    rgb_leds[rgb_led_row][rgb_led_col].setIG(val);
}

void Grid::setIB(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val) {
    rgb_leds[rgb_led_row][rgb_led_col].setIB(val);
}

void Grid::setI3(uint8_t rgb_led_row, uint8_t rgb_led_col,
                   uint8_t r_val, uint8_t g_val, uint8_t b_val) {
    rgb_leds[rgb_led_row][rgb_led_col].setI3(r_val, g_val, b_val);
}

void Grid::setI3(uint8_t rgb_led_row, uint8_t rgb_led_col, uint8_t val) {
    rgb_leds[rgb_led_row][rgb_led_col].setI3(val);
}

void Grid::setIRAll(uint8_t val) {
    for (uint8_t i=0; i<rgb_leds.size(); i++) {
        for (uint8_t j=0; j<rgb_leds[0].size(); j++) {
            rgb_leds[i][j].setIR(val);
        }
    }
}

void Grid::setIGAll(uint8_t val) {
    for (uint8_t i=0; i<rgb_leds.size(); i++) {
        for (uint8_t j=0; j<rgb_leds[0].size(); j++) {
            rgb_leds[i][j].setIG(val);
        }
    }
}

void Grid::setIBAll(uint8_t val) {
    for (uint8_t i=0; i<rgb_leds.size(); i++) {
        for (uint8_t j=0; j<rgb_leds[0].size(); j++) {
            rgb_leds[i][j].setIB(val);
        }
    }
}

void Grid::setI3All(uint8_t r_val, uint8_t g_val, uint8_t b_val) {
    for (uint8_t i=0; i<rgb_leds.size(); i++) {
        for (uint8_t j=0; j<rgb_leds[0].size(); j++) {
            rgb_leds[i][j].setI3(r_val, g_val, b_val);
        }
    }
}

void Grid::setI3All(uint8_t val) {
    for (uint8_t i=0; i<led_drvs.size(); i++) {
        led_drvs[i].setLEDIAll(val);
    }
}


uint16_t Grid::getV(uint8_t rgb_led_row, uint8_t rgb_led_col) {
    return rgb_leds[rgb_led_row][rgb_led_col].getV();
}


