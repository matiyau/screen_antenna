//
// Created by n7 on 2/6/23.
//

#include "conn_main.h"
#include "ad_conv.h"
#include "led_drv.h"
#include "grid.h"
#include "rgb_led.h"

Grid create_grid() {
    Grid grid = Grid(4, 4, 2, 2);

    grid.assignLEDDrvAddr(0, LED_DRV_0_ADDR);
    grid.assignLEDDrvAddr(1, LED_DRV_1_ADDR);

    grid.assignADConvShdnPin(0, ADC_0_SHDN);
    grid.assignADConvShdnPin(1, ADC_1_SHDN);

    grid.connectRGBLEDToLEDDrv(0, 0, 0, LED_0_0_R_TX_PORT, LED_0_0_G_TX_PORT,
                               LED_0_0_B_TX_PORT);
    grid.connectRGBLEDToADConv(0, 0, 0, LED_0_0_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(0, 1, 0, LED_0_1_R_TX_PORT, LED_0_1_G_TX_PORT,
                               LED_0_1_B_TX_PORT);
    grid.connectRGBLEDToADConv(0, 1, 0, LED_0_1_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(0, 2, 0, LED_0_2_R_TX_PORT, LED_0_2_G_TX_PORT,
                               LED_0_2_B_TX_PORT);
    grid.connectRGBLEDToADConv(0, 2, 0, LED_0_2_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(0, 3, 0, LED_0_3_R_TX_PORT, LED_0_3_G_TX_PORT,
                               LED_0_3_B_TX_PORT);
    grid.connectRGBLEDToADConv(0, 3, 0, LED_0_3_R_RX_CHAN);

    grid.connectRGBLEDToLEDDrv(1, 0, 0, LED_1_0_R_TX_PORT, LED_1_0_G_TX_PORT,
                               LED_1_0_B_TX_PORT);
    grid.connectRGBLEDToADConv(1, 0, 0, LED_1_0_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(1, 1, 0, LED_1_1_R_TX_PORT, LED_1_1_G_TX_PORT,
                               LED_1_1_B_TX_PORT);
    grid.connectRGBLEDToADConv(1, 1, 0, LED_1_1_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(1, 2, 0, LED_1_2_R_TX_PORT, LED_1_2_G_TX_PORT,
                               LED_1_2_B_TX_PORT);
    grid.connectRGBLEDToADConv(1, 2, 0, LED_1_2_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(1, 3, 0, LED_1_3_R_TX_PORT, LED_1_3_G_TX_PORT,
                               LED_1_3_B_TX_PORT);
    grid.connectRGBLEDToADConv(1, 3, 0, LED_1_3_R_RX_CHAN);

    grid.connectRGBLEDToLEDDrv(2, 0, 0, LED_2_0_R_TX_PORT, LED_2_0_G_TX_PORT,
                               LED_2_0_B_TX_PORT);
    grid.connectRGBLEDToADConv(2, 0, 0, LED_2_0_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(2, 1, 0, LED_2_1_R_TX_PORT, LED_2_1_G_TX_PORT,
                               LED_2_1_B_TX_PORT);
    grid.connectRGBLEDToADConv(2, 1, 0, LED_2_1_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(2, 2, 0, LED_2_2_R_TX_PORT, LED_2_2_G_TX_PORT,
                               LED_2_2_B_TX_PORT);
    grid.connectRGBLEDToADConv(2, 2, 0, LED_2_2_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(2, 3, 0, LED_2_3_R_TX_PORT, LED_2_3_G_TX_PORT,
                               LED_2_3_B_TX_PORT);
    grid.connectRGBLEDToADConv(2, 3, 0, LED_2_3_R_RX_CHAN);

    grid.connectRGBLEDToLEDDrv(3, 0, 0, LED_3_0_R_TX_PORT, LED_3_0_G_TX_PORT,
                               LED_3_0_B_TX_PORT);
    grid.connectRGBLEDToADConv(3, 0, 0, LED_3_0_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(3, 1, 0, LED_3_1_R_TX_PORT, LED_3_1_G_TX_PORT,
                               LED_3_1_B_TX_PORT);
    grid.connectRGBLEDToADConv(3, 1, 0, LED_3_1_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(3, 2, 0, LED_3_2_R_TX_PORT, LED_3_2_G_TX_PORT,
                               LED_3_2_B_TX_PORT);
    grid.connectRGBLEDToADConv(3, 2, 0, LED_3_2_R_RX_CHAN);
    grid.connectRGBLEDToLEDDrv(3, 3, 0, LED_3_3_R_TX_PORT, LED_3_3_G_TX_PORT,
                               LED_3_3_B_TX_PORT);
    grid.connectRGBLEDToADConv(3, 3, 0, LED_3_3_R_RX_CHAN);

    return grid;
};