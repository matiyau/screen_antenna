//
// Created by n7 on 8/6/23.
//

#include "tx.h"
#include "settings.h"
#include "sketch_main.h"

void txStby(Params &prms) {
    if ((prms.slot_id == TX_STBY_SLOTS) && (prms.subslot_id==1)) {
        prms.tx_stage = TX_PRMB;
        prms.slot_id = 254;
    }
}

void txPrmb(Params &prms) {
    if (prms.subslot_id==0) {
        return;
    }
    if (prms.slot_id == 0) {
        for (LED led: prms.tx_leds) {
            grid.setIR(led.pos[0], led.pos[1], 255);
        }
    }
    else if (prms.slot_id == PRMB_SLOTS/2) {
        for (LED led: prms.tx_leds) {
            grid.setIR(led.pos[0], led.pos[1], 0);
        }
    }
    else if (prms.slot_id == PRMB_SLOTS-1) {
        Serial.println("Pr");
        prms.tx_stage = TX_TRGT;
        prms.slot_id = 254;
    }
}

void txTrgt(Params &prms) {
    if (prms.subslot_id == 0) {
        for (LED led: prms.tx_leds) {
            grid.setIR(led.pos[0], led.pos[1], 0);
        }
    }
    else if (prms.subslot_id == 1) {
        for (LED led: prms.tx_leds) {
            if (prms.slot_id < led.trgt) {
                grid.setIR(led.pos[0], led.pos[1], 255);
            }
        }
        if (prms.slot_id == 254) {
            Serial.println("Tg");
            prms.tx_stage = TX_SIZE;
            prms.bit_count = 0;
            prms.next_bit = (prms.data_size >> 31) & 0x01;
            prms.active = false;
        }
    }
}

void txSize(Params &prms) {
    if (prms.subslot_id == 0) {
        for (LED led: prms.tx_leds) {
            if (prms.slot_id < led.trgt) {
                grid.setIR(led.pos[0], led.pos[1], prms.next_bit ? 0 : 255);
            }
            else if (prms.slot_id == led.trgt) {
                grid.setIR(led.pos[0], led.pos[1], 0);
            }
        }
    }
    else if (prms.subslot_id == 1) {
        for (LED led: prms.tx_leds) {
            if (prms.slot_id < led.trgt) {
                grid.setIR(led.pos[0], led.pos[1], prms.next_bit ? 255 : 0);
                prms.active = true;
            }
        }
        if (prms.active == false) {
            return;
        }
        prms.active = false;
        if ((++prms.bit_count) == 32) {
            Serial.println("Sz");
            prms.tx_stage = TX_DATA;
            prms.bit_count = 0;
            prms.byte_count = 0;
            prms.next_bit = (prms.data[0] >> 7) & 0x01;
        }
        else {
            prms.next_bit = (prms.data_size >> (31 - prms.bit_count)) & 0x01;
        }
    }
}

void txData(Params &prms) {
    if (prms.subslot_id == 0) {
        for (LED led: prms.tx_leds) {
            if (prms.slot_id < led.trgt) {
                grid.setIR(led.pos[0], led.pos[1], prms.next_bit ? 0 : 255);
            }
            else if (prms.slot_id == led.trgt) {
                grid.setIR(led.pos[0], led.pos[1], 0);
            }
        }
        if (prms.byte_count == prms.data_size) {
            timer.stop();
            prms.mode = RX;
            prms.rx_stage = RX_STBY;
            for (LED led: prms.tx_leds) {
                grid.setIR(led.pos[0], led.pos[1], 0);
            }
            Serial.println("Dt");
            Serial.print(UART_CMD_STT);
            for (uint32_t i=0; i<prms.data_size; i++) {
                Serial.println(prms.data[i]);
            }
            Serial.println(UART_CMD_END);
            return;
        }
    }
    else if (prms.subslot_id == 1) {
        for (LED led: prms.tx_leds) {
            if (prms.slot_id < led.trgt) {
                grid.setIR(led.pos[0], led.pos[1], prms.next_bit ? 255 : 0);
                prms.active = true;
            }
        }
        if (prms.active == false) {
            return;
        }
        prms.active = false;
        if ((++prms.bit_count) == 8) {
            prms.bit_count = 0;
            ;
            if ((++prms.byte_count) < prms.data_size) {
                prms.next_bit = (prms.data[prms.byte_count] >> 7) & 0x01;
            }
            else {
                prms.next_bit = false;
            }
        }
        else {
            prms.next_bit = (prms.data[prms.byte_count] >>
                             (7-prms.bit_count)) & 0x01;
        }
    }
}

void txTick(Params &prms) {
    if (prms.tx_stage == TX_STBY) {
        txStby(prms);
    }
    else if (prms.tx_stage == TX_PRMB) {
        txPrmb(prms);
    }
    else if (prms.tx_stage == TX_TRGT) {
        txTrgt(prms);
    }
    else if (prms.tx_stage == TX_SIZE) {
        txSize(prms);
    }
    else if (prms.tx_stage == TX_DATA) {
        txData(prms);
    }
}
