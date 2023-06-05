//
// Created by n7 on 8/12/22.
//

#include <SPI.h>

#include "ad_conv.h"

void ADConv::assignShdnPin(uint8_t shdn_pin) {
    if (shdn_pin != shdn_pin_) {
        init_done_ = false;
    }
    shdn_pin_ = shdn_pin;
}

void ADConv::assignFreqHz(uint32_t freq_hz) {
    freq_hz_ = freq_hz;
}

void ADConv::begin() {
    SPI.begin(shdn_pin_);
    init_done_ = true;
}

uint16_t ADConv::readChan(uint8_t chan) {
    if (!init_done_) {
        return -1;
    }
    buf_[0] = 0x01;
    buf_[1] = (0x08 | chan) << 4;
    SPI.beginTransaction(shdn_pin_, SPISettings(freq_hz_, MSBFIRST,
                                                SPI_MODE0));
    SPI.transfer(shdn_pin_, buf_, 3);
    SPI.endTransaction();
    return (((uint16_t)(buf_[1] & 0x07)) << 8) | buf_[2];
}
