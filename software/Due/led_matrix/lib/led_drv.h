//
// Created by n7 on 8/12/22.
//

#ifndef INC_8X8_LED_DRV_H
#define INC_8X8_LED_DRV_H

#include <cstdint>

class LEDDrv {
    uint8_t addr_;

public:
    LEDDrv() = default;

    LEDDrv(uint8_t addr);

    void SetAddr(uint8_t addr);

};


#endif //INC_8X8_LED_DRV_H
