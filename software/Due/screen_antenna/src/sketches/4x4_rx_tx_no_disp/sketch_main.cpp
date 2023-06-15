//
// Created by n7 on 8/6/23.
//

#include "sketch_main.h"
#include "rx.h"
#include "types.h"
#include "tx.h"
#include "uart.h"

Params params;

void onTick(void *args) {
    Params &prms = *((Params *)args);
    prms.subslot_id = (prms.subslot_id + 1) % 2;
    if (prms.subslot_id == 0) {
        if (++prms.slot_id == 255) {
            prms.slot_id = 0;
        }
    }

    if (prms.mode == RX) {
        if (prms.subslot_id == 1) {
            // Only runs on second subslot:
            rxTick(prms);
        }
    }
    else if (prms.mode==TX) {
        txTick(prms);
    }
}


void setupCust() {
    timer.setHandler(onTick);
#ifdef MAT
    params.mode = TX;
    params.tx_stage = TX_STBY;
    params.tx_leds.push_back({{2, 1}, 255});
    params.data_size = TX_DATA_SZ;
    params.subslot_id = 1;
    params.slot_id = 254;
    for (uint32_t i=0; i < TX_DATA_SZ; i++) {
        params.data[i] = random(0, 256);
    }
    delay(1000);
    timer.start();
#else
    params.mode = RX;
    params.rx_stage = RX_STBY;
    params.rx_led = {{2, 2}, 255};
    params.subslot_id = 1;
    params.slot_id = 254;
#endif
}

void loop() {
    parseUARTCmd(params);
    timer.handle((void *)(&params));
    if ((params.mode == RX) && (params.rx_stage == RX_STBY)) {
        rxStby(params);
    }
}
