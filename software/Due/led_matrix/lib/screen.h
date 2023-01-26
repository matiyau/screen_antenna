//
// Created by n7 on 8/12/22.
//

#ifndef INC_8X8_SCREEN_H
#define INC_8X8_SCREEN_H

#include <cstdint>
#include <vector>

#include "adc.h"
#include "led_drv.h"
#include "rgb_led.h"


class Screen {
    std::vector<std::vector<RGBLED>> rgb_leds_;
    std::vector<LEDDrv> led_drvs_;
    std::vector<ADC> adcs_;

public:
    Screen(uint8_t n_rows, uint8_t n_cols, uint8_t n_drvs, uint8_t n_adcs);

    void CfgLEDConn(uint8_t row, uint8_t col, uint8_t drv_id, uint8_t drv_ch_r,
                    uint8_t drv_ch_g, uint8_t drv_ch_b, uint8_t adc_id_r,
                    uint8_t adc_ch_r);

    void CfgLEDDrvAddr(uint8_t drv_id, uint8_t addr);


};


#endif //INC_8X8_SCREEN_H
