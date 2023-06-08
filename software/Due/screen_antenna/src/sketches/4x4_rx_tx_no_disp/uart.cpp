//
// Created by n7 on 8/6/23.
//

#include <Arduino.h>
// To prevent max and min overrides by Arduino library
#undef max
#undef min

#include "uart.h"
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
//        *r,2,2#
        prms.rx_led.pos[0] = Serial.parseInt();
        prms.rx_led.pos[1] = Serial.parseInt();
        prms.mode = RX;
    }
    else if (c == 't') {
//        *t,2,0,45,2,1,115,2,2,175,2,3,20#
        prms.tx_leds.clear();
        while (true) {
            while (Serial.available() < 1);
            char d = Serial.read();
            if (d == UART_CMD_END) {
                break;
            }
            prms.tx_leds.push_back({{(uint8_t)Serial.parseInt(),
                                       (uint8_t)Serial.parseInt()},
                                      (uint8_t)Serial.parseInt()});
        }
        prms.mode = TX;
    }
}