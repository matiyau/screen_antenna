//
// Created by n7 on 8/12/22.
//

#ifndef SCREEN_ANTENNA_LED_DRV_H
#define SCREEN_ANTENNA_LED_DRV_H

#include <cstdint>

#define REG_GRP_PWM 0x08
#define REG_GRP_FREQ 0x09

#define REG_PWM_LED_0 0x0A
#define REG_PWM_LED_1 0x0B
#define REG_PWM_LED_2 0x0C
#define REG_PWM_LED_3 0x0D
#define REG_PWM_LED_4 0x0E
#define REG_PWM_LED_5 0x0F
#define REG_PWM_LED_6 0x10
#define REG_PWM_LED_7 0x11
#define REG_PWM_LED_8 0x12
#define REG_PWM_LED_9 0x13
#define REG_PWM_LED_10 0x14
#define REG_PWM_LED_11 0x15
#define REG_PWM_LED_12 0x16
#define REG_PWM_LED_13 0x17
#define REG_PWM_LED_14 0x18
#define REG_PWM_LED_15 0x19
#define REG_PWM_LED_16 0x1A
#define REG_PWM_LED_17 0x1B
#define REG_PWM_LED_18 0x1C
#define REG_PWM_LED_19 0x1D
#define REG_PWM_LED_20 0x1E
#define REG_PWM_LED_21 0x1F
#define REG_PWM_LED_22 0x20
#define REG_PWM_LED_23 0x21
#define REG_PWM_LED_ALL 0x3F

#define REG_I_LED_0 0x22
#define REG_I_LED_1 0x23
#define REG_I_LED_2 0x24
#define REG_I_LED_3 0x25
#define REG_I_LED_4 0x26
#define REG_I_LED_5 0x27
#define REG_I_LED_6 0x28
#define REG_I_LED_7 0x29
#define REG_I_LED_8 0x2A
#define REG_I_LED_9 0x2B
#define REG_I_LED_10 0x2C
#define REG_I_LED_11 0x2D
#define REG_I_LED_12 0x2E
#define REG_I_LED_13 0x2F
#define REG_I_LED_14 0x30
#define REG_I_LED_15 0x31
#define REG_I_LED_16 0x32
#define REG_I_LED_17 0x33
#define REG_I_LED_18 0x34
#define REG_I_LED_19 0x35
#define REG_I_LED_20 0x36
#define REG_I_LED_21 0x37
#define REG_I_LED_22 0x38
#define REG_I_LED_23 0x39
#define REG_I_LED_ALL 0x40

class LEDDrv {
    uint8_t addr_;

public:
    LEDDrv() {};

    LEDDrv(uint8_t addr) : addr_(addr) {};

    void assignAddr(uint8_t addr);
    void setLEDPWM(uint8_t chan, uint8_t val);
    void setLEDPWMAll(uint8_t val);

    void setLEDI(uint8_t chan, uint8_t val);
    void setLEDIAll(uint8_t val);

    void setLEDGrpPWM(uint8_t val);
    void setLEDGrpFreq(uint8_t val);

    void setRegister(uint8_t num, uint8_t val);
};


#endif //SCREEN_ANTENNA_LED_DRV_H
