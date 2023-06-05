#include <Arduino.h>
// To prevent max and min overrides by Arduino library
#undef max
#undef min

#include "grid.h"
#include "settings.h"

#include "connections/conn_main.h"

Grid grid = create_grid();

void setup() {
    grid.begin(UART_BAUD_RATE, I2C_FREQ_HZ, SPI_FREQ_HZ);
}

void loop() {
}