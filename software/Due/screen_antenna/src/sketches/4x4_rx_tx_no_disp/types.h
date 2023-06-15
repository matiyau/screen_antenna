//
// Created by n7 on 8/6/23.
//

#ifndef SCREEN_ANTENNA_TYPES_H
#define SCREEN_ANTENNA_TYPES_H

#include <cstdint>
#include <vector>

#include "sketch_main.h"

enum Mode {
    RX,
    TX
};

enum RxStage {
    RX_STBY,
    RX_PRMB,
    RX_TRGT,
    RX_SIZE,
    RX_DATA
};

enum TxStage {
    TX_STBY,
    TX_PRMB,
    TX_TRGT,
    TX_SIZE,
    TX_DATA
};

struct LED {
    uint8_t pos[2];
    uint8_t trgt;
};

struct Params {
    Mode mode;
    LED rx_led;
    std::vector<LED> tx_leds;
    union {
        RxStage rx_stage;
        TxStage tx_stage;
    };
    uint8_t slot_id;
    uint8_t subslot_id;
    uint8_t data[10000];
    bool next_bit;
    uint16_t byte_count;
    uint32_t data_size;
    uint8_t bit_count;
    unsigned long start_tm_us;
    unsigned long end_tm_us;
    bool active;
};

#endif //SCREEN_ANTENNA_TYPES_H
