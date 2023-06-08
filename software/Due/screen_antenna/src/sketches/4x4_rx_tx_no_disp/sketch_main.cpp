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
    if (prms.mode == RX) {
       rxTick(prms);
    }
    else if (prms.mode==TX) {
        txTick(prms);
    }
}


void setupCust() {
    timer.setHandler(onTick);
}

void loop() {
    parseUARTCmd(params);
    timer.handle((void *)(&params));
}
