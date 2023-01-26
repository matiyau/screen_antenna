//
// Created by n7 on 8/12/22.
//

#include "screen.h"

Screen::Screen(uint8_t n_rows, uint8_t n_cols, uint8_t n_drvs,
               uint8_t n_adcs) {
    rgb_leds_.assign(n_rows, std::vector<RGBLED>(n_cols, RGBLED()));
    led_drvs_.assign(n_drvs, LEDDrv());
    adcs_.assign(n_adcs, ADC());
}

void
Screen::CfgLEDConn(uint8_t row, uint8_t col, uint8_t drv_id, uint8_t drv_ch_r,
                   uint8_t drv_ch_g, uint8_t drv_ch_b, uint8_t adc_id_r,
                   uint8_t adc_ch_r) {
    rgb_leds_[row][col].SetDrv(drv_id, drv_ch_r, drv_ch_g, drv_ch_b);
    rgb_leds_[row][col].SetADC(adc_id_r, adc_ch_r);
}

void Screen::CfgLEDDrvAddr(uint8_t drv_id, uint8_t addr) {
    led_drvs_[drv_id].SetAddr(addr);
}
