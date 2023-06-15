//
// Created by n7 on 8/6/23.
//

#include <Arduino.h>
// To prevent max and min overrides by Arduino library
#undef max
#undef min

#include "uart.h"

#include "main.h"
#include "settings.h"

void parseUARTCmd(Params &prms) {
    if (Serial.available() < 2) {
        return;
    }
    if (Serial.read() != UART_CMD_STT) {
        return;
    }

    char c = Serial.read();
    if (c == 'r') {
//        *r,100,2,2#
        timer.stop();
        timer.setPeriod(Serial.parseInt());
        prms.rx_led.pos[0] = Serial.parseInt();
        prms.rx_led.pos[1] = Serial.parseInt();
        prms.mode = RX;
        prms.rx_stage = RX_STBY;
        prms.subslot_id = 1;
        prms.slot_id = 254;
    }
    else if (c == 't') {
//        *t,100,2,0,45,2,1,115,2,2,175,2,3,20#
        timer.stop();
        timer.setPeriod(Serial.parseInt());
        prms.tx_leds.clear();
        uint16_t total_trgt = 0;
        while (true) {
            while (Serial.available() < 1);
            char d = Serial.read();
            if (d == UART_CMD_END) {
                break;
            }
            prms.tx_leds.push_back({{(uint8_t)Serial.parseInt(),
                                       (uint8_t)Serial.parseInt()},
                                      (uint8_t)Serial.parseInt()});
            total_trgt += prms.tx_leds.back().trgt;
        }
        total_trgt = (total_trgt > 255) ? 255 : total_trgt;
        prms.mode = TX;
        prms.tx_stage = TX_STBY;
        prms.subslot_id = 1;
        prms.slot_id = 254;
        prms.data_size = (TX_DATA_SZ*total_trgt*100)/(255*timer.getPeriod());
        for (uint32_t i=0; i < prms.data_size; i++) {
            prms.data[i] = random(0, 256);
        }
        timer.start();
    }
}