//
// Created by n7 on 8/6/23.
//

#include "rx.h"

#include "main.h"
#include "settings.h"

void rxStby(Params &prms) {
    timer.start();
    int16_t vRel = grid.getVRel(prms.rx_led.pos[0], prms.rx_led.pos[1]);
    if (vRel > ADC_V_THRESH_PRMB) {
        prms.rx_stage = RX_PRMB;
        prms.slot_id = 0;
        prms.subslot_id = 1;
    }
    else {
        timer.stop();
    }
}

void rxPrmb(Params &prms) {
    int16_t vRel = grid.getVRel(prms.rx_led.pos[0], prms.rx_led.pos[1]);
    if (vRel <= ADC_V_THRESH_PRMB) {
//        Serial.println(prms.slot_id);
        if (prms.slot_id <= (PRMB_SLOTS/2)-3) {
            timer.stop();
            prms.rx_stage = RX_STBY;
            prms.subslot_id = 1;
            prms.slot_id = 254;
        }
        else if (prms.slot_id < PRMB_SLOTS/2) {
            prms.slot_id = (PRMB_SLOTS/2);
        }
        else if (prms.slot_id == PRMB_SLOTS-1) {
            prms.active = true;
            prms.rx_stage = RX_TRGT;
            prms.rx_led.trgt = 0;
            prms.slot_id = 254;
            Serial.println("Pr");
        }
    }
}

void rxTrgt(Params &prms) {
    delayMicroseconds(ADC_READ_DELAY_US);
    if (grid.getVRel(prms.rx_led.pos[0], prms.rx_led.pos[1]) >
    ADC_V_THRESH_TRGT) {
        if (prms.active) {
            prms.rx_led.trgt++;
        }
    }
    else {
        prms.active = false;
    }
    if (prms.slot_id == 254) {
        Serial.print("Tg: ");
        Serial.println(prms.rx_led.trgt);
        prms.rx_stage = RX_SIZE;
        prms.data_size = 0;
        prms.bit_count = 0;
    }
}

void rxSize(Params &prms) {
    delayMicroseconds(ADC_READ_DELAY_US);
    int16_t vRel = grid.getVRel(prms.rx_led.pos[0], prms.rx_led.pos[1]);
//    Serial.println(micros());
    if (prms.slot_id >= prms.rx_led.trgt) {
        return;
    }
    prms.data_size = prms.data_size << 1;
    if (vRel > ADC_V_THRESH_SIZE) {
        prms.data_size = prms.data_size | 0x01;
    }
    if ((++prms.bit_count) == 32) {
        Serial.print("Sz: ");
        Serial.println(prms.data_size);
        prms.data_size = (TX_DATA_SZ*prms.rx_led.trgt*100)/(255*timer.getPeriod());
        Serial.print("New Sz: ");
        Serial.println(prms.data_size);
        prms.rx_stage = RX_DATA;
        prms.bit_count = 0;
        prms.byte_count = 0;
        prms.start_tm_us = micros();
    }
}

void rxData(Params &prms) {
    delayMicroseconds(ADC_READ_DELAY_US);
    int16_t vRel = grid.getVRel(prms.rx_led.pos[0], prms.rx_led.pos[1]);
//    Serial.println(micros());
    if (prms.byte_count == prms.data_size) {
        if (prms.slot_id == 254) {
            prms.end_tm_us = micros();
            timer.stop();
            prms.rx_stage = RX_STBY;
            Serial.println("Dt:");
            Serial.print(UART_CMD_STT);
            for (uint16_t i=0; i<prms.data_size; i++) {
                Serial.println(prms.data[i]);
            }
            Serial.println(UART_CMD_END);
            Serial.print("Start: ");
            Serial.println(prms.start_tm_us);
            Serial.print("End: ");
            Serial.println(prms.end_tm_us);
            Serial.print("Net: ");
            Serial.println(prms.end_tm_us - prms.start_tm_us);
        }
        return;
    }
    if (prms.slot_id >= prms.rx_led.trgt) {
        return;
    }
    prms.data[prms.byte_count] = prms.data[prms.byte_count] << 1;
    if (vRel > ADC_V_THRESH_DATA) {
        prms.data[prms.byte_count] = prms.data[prms.byte_count] | 0x01;
    }
    if ((++prms.bit_count) == 8) {
        prms.bit_count = 0;
        prms.byte_count++;
    }

}

void rxTick(Params &prms) {
     if (prms.rx_stage == RX_PRMB) {
        rxPrmb(prms);
    }
    else if (prms.rx_stage == RX_TRGT) {
        rxTrgt(prms);
    }
    else if (prms.rx_stage == RX_SIZE) {
        rxSize(prms);
    }
    else if (prms.rx_stage == RX_DATA) {
        rxData(prms);
    }
}
