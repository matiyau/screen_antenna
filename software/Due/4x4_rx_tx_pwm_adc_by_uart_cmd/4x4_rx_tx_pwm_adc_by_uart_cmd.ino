#include "includes.h"

#define ADC_THRESH 20

PCA9956 led_drivers[2]{&Wire, &Wire};
Adafruit_MCP3008 adcs[2];

RGBLED rgb_leds[4][4] = {{RGBLED(led_drivers[0], LED_0_0_R_TX_PORT, LED_0_0_G_TX_PORT, LED_0_0_B_TX_PORT, adcs[0], LED_0_0_R_RX_CHAN),
                            RGBLED(led_drivers[0], LED_0_1_R_TX_PORT, LED_0_1_G_TX_PORT, LED_0_1_B_TX_PORT, adcs[0], LED_0_1_R_RX_CHAN),
                            RGBLED(led_drivers[0], LED_0_2_R_TX_PORT, LED_0_2_G_TX_PORT, LED_0_2_B_TX_PORT, adcs[0], LED_0_2_R_RX_CHAN),
                            RGBLED(led_drivers[0], LED_0_3_R_TX_PORT, LED_0_3_G_TX_PORT, LED_0_3_B_TX_PORT, adcs[0], LED_0_3_R_RX_CHAN)},
                         {RGBLED(led_drivers[0], LED_1_0_R_TX_PORT, LED_1_0_G_TX_PORT, LED_1_0_B_TX_PORT, adcs[0], LED_0_0_R_RX_CHAN),
                            RGBLED(led_drivers[0], LED_1_1_R_TX_PORT, LED_1_1_G_TX_PORT, LED_1_1_B_TX_PORT, adcs[0], LED_0_1_R_RX_CHAN),
                            RGBLED(led_drivers[0], LED_1_2_R_TX_PORT, LED_1_2_G_TX_PORT, LED_1_2_B_TX_PORT, adcs[0], LED_0_2_R_RX_CHAN),
                            RGBLED(led_drivers[0], LED_1_3_R_TX_PORT, LED_1_3_G_TX_PORT, LED_1_3_B_TX_PORT, adcs[0], LED_0_3_R_RX_CHAN)},
                         {RGBLED(led_drivers[1], LED_2_0_R_TX_PORT, LED_2_0_G_TX_PORT, LED_2_0_B_TX_PORT, adcs[1], LED_2_0_R_RX_CHAN),
                            RGBLED(led_drivers[1], LED_2_1_R_TX_PORT, LED_2_1_G_TX_PORT, LED_2_1_B_TX_PORT, adcs[1], LED_2_1_R_RX_CHAN),
                            RGBLED(led_drivers[1], LED_2_2_R_TX_PORT, LED_2_2_G_TX_PORT, LED_2_2_B_TX_PORT, adcs[1], LED_2_2_R_RX_CHAN),
                            RGBLED(led_drivers[1], LED_2_3_R_TX_PORT, LED_2_3_G_TX_PORT, LED_2_3_B_TX_PORT, adcs[1], LED_2_3_R_RX_CHAN)},
                         {RGBLED(led_drivers[1], LED_3_0_R_TX_PORT, LED_3_0_G_TX_PORT, LED_3_0_B_TX_PORT, adcs[1], LED_3_0_R_RX_CHAN),
                            RGBLED(led_drivers[1], LED_3_1_R_TX_PORT, LED_3_1_G_TX_PORT, LED_3_1_B_TX_PORT, adcs[1], LED_3_1_R_RX_CHAN),
                            RGBLED(led_drivers[1], LED_3_2_R_TX_PORT, LED_3_2_G_TX_PORT, LED_3_2_B_TX_PORT, adcs[1], LED_3_2_R_RX_CHAN),
                            RGBLED(led_drivers[1], LED_3_3_R_TX_PORT, LED_3_3_G_TX_PORT, LED_3_3_B_TX_PORT, adcs[1], LED_3_3_R_RX_CHAN)}};

state_t state = RX_STANDBY;

int16_t led_r_rx_ambs[4][4];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while(!Serial);

  Wire.begin(); // Wire needs to init separately...
  Wire.setClock(1000000);

  led_drivers[0].init(LED_DRV_0_ADDR, 0, true);
  led_drivers[1].init(LED_DRV_1_ADDR, 0, true);
  adcs[0].begin(ADC_0_SHDN);
  adcs[1].begin(ADC_1_SHDN);

  led_drivers[0].setSingleRegister(0x3F, 255); //PWM All
  led_drivers[1].setSingleRegister(0x3F, 255); //PWM All

  delay(500);

  for (uint8_t i=0; i<4; i++) {
    for (uint8_t j=0; j<4; j++) {
      led_r_rx_ambs[i][j] = rgb_leds[i][j].getADCR();
      Serial.print(led_r_rx_ambs[i][j]);
      Serial.print("\t");
    }
    Serial.println();
  }
  Serial.println();

}

void loop() {
  if (Serial.available() < 2) {
    return;
  }
  if (Serial.read() != CMD_STT) {
    return;
  }
  char c = Serial.read();
  if (c == 'g') {
    //Get
    uint8_t i = Serial.parseInt();
    uint8_t j = Serial.parseInt();

    Serial.print("*");
    Serial.print(rgb_leds[i][j].getADCR() - led_r_rx_ambs[i][j]);
    Serial.print("#");
  }
  else if (c == 'G') {
    //Get All
    Serial.println("*");
    for (uint8_t i=0; i<4; i++) {
      for (uint8_t j=0; j<4; j++) {
        Serial.print(rgb_leds[i][j].getADCR() - led_r_rx_ambs[i][j]);
        Serial.print("\t");
      }
    Serial.println();
  }
  Serial.println();
    Serial.print("#");
  }
  else if (c == 's') {
    //Set
    uint8_t i = Serial.parseInt();
    uint8_t j = Serial.parseInt();
    uint8_t chan = Serial.parseInt();
    uint8_t val = Serial.parseInt();
    if (chan == 0) {
      rgb_leds[i][j].setIR(val);
    }
    else if (chan == 1) {
      rgb_leds[i][j].setIG(val);      
    }
    else if (chan == 2) {
      rgb_leds[i][j].setIB(val);      
    }
  }
}
