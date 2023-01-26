//
// Created by n7 on 8/12/22.
//

#ifndef INC_8X8_RGB_LED_H
#define INC_8X8_RGB_LED_H

#include <cstdint>


class RGBLED {
    uint8_t drv_id_;
    uint8_t drv_ch_r_;
    uint8_t drv_ch_g_;
    uint8_t drv_ch_b_;

    uint8_t adc_id_r_;
    uint8_t adc_ch_r_;

public:
    RGBLED() = default;

    RGBLED(uint8_t drv_id, uint8_t drv_ch_r, uint8_t drv_ch_g,
           uint8_t drv_ch_b, uint8_t adc_id_r, uint8_t adc_ch_r);

    void SetDrv(uint8_t drv_id, uint8_t drv_ch_r, uint8_t drv_ch_g,
                uint8_t drv_ch_b);

    void SetADC(uint8_t adc_id_r, uint8_t adc_ch_r);

};


#endif //INC_8X8_RGB_LED_H
