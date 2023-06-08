#include <Arduino.h>
// To prevent max and min overrides by Arduino library
#undef max
#undef min

#include "main.h"
#include "settings.h"

#include "connections/conn_main.h"

Grid grid = createGrid();
TimerMod timer(0);

void setup() {
    grid.begin(UART_BAUD_RATE, I2C_FREQ_HZ, SPI_FREQ_HZ);
    setupCust();
}
