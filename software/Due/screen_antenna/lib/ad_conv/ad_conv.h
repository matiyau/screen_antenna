//
// Created by n7 on 8/12/22.
//

#ifndef SCREEN_ANTENNA_AD_CONV_H
#define SCREEN_ANTENNA_AD_CONV_H

#include <cstdint>

class ADConv {
    uint8_t shdn_pin_;
    uint32_t freq_hz_;
    uint8_t buf_[3] = {0x01, 0x00, 0x00};
    bool init_done_ = false;

public:
    ADConv() {};

    ADConv(uint32_t freq_hz): freq_hz_(freq_hz) {};

    ADConv(uint8_t shdn_pin, uint32_t freq_hz):
        shdn_pin_(shdn_pin), freq_hz_(freq_hz) {};

    void assignShdnPin(uint8_t shdn_pin);

    void assignFreqHz(uint32_t freq_hz);

    void begin();

    uint16_t readChan(uint8_t chan);
};


#endif //SCREEN_ANTENNA_AD_CONV_H
