//
// Created by n7 on 8/6/23.
//

#ifndef SCREEN_ANTENNA_TYPES_H
#define SCREEN_ANTENNA_TYPES_H

#include <cstdint>
#include <vector>

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
    uint8_t targ;
};

struct Params {
    Mode mode = RX;
    LED rx_led;
    std::vector<LED> tx_leds;
    union {
        RxStage rx_stage = RX_STBY;
        TxStage tx_stage;
    };
    uint8_t slot_count = 0;
    uint8_t subslot_count = 0;
    uint8_t data[100] = {0};
};

#endif //SCREEN_ANTENNA_TYPES_H
