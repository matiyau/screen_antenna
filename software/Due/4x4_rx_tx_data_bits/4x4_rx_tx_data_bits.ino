#include "includes.h"

#define ADC_THRESH 20
#define BURST_TM_US 13600
#define MAX_SAMPLES 15000
#define TX_BITS_COUNT 4

#define TX_MAX_SLOTS 8

PCA9956 led_drivers[2]{&Wire, &Wire};
Adafruit_MCP3008 adcs[2];

uint8_t tx_bits[TX_BITS_COUNT] = {0, 0, 1, 1};
uint8_t tx_bit_pos = 0;
uint8_t tx_half_cycle = 0;
uint8_t tx_led_I = 255;

typedef struct __attribute__((__packed__)) {
  unsigned long t;
  int16_t v;
} adc_sample_t;

adc_sample_t adc_samps[MAX_SAMPLES];

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

uint8_t tx_leds_count = 0;
uint8_t tx_slot_id = 0;
uint8_t tx_leds_coords[16][2] = {0};
uint8_t tx_leds_targets[16] = {0};
uint8_t tx_leds_targets_pending[16] = {0};
bool tx_active, tx_led_change, tx_reset;

int16_t led_r_rx_ambs[4][4];

bool end_sampling = false;

void handler_end_sampling() {
  end_sampling = true;
}

bool tx_tick = false;
uint8_t tx_led_id = 255, tx_led_id_prev=255;

void handler_tx() {
  tx_tick = true;
}

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
  if (tx_tick) {
    if (tx_active) {
      rgb_leds[tx_leds_coords[tx_led_id][0]][tx_leds_coords[tx_led_id][1]].setIR(tx_led_I);
      for (uint8_t i=tx_led_id+1; i<tx_leds_count; i++) {
        if (TX_MAX_SLOTS - tx_slot_id <= tx_leds_targets_pending[i]) {
          rgb_leds[tx_leds_coords[i][0]][tx_leds_coords[i][1]].setIR(tx_led_I);
          if (tx_half_cycle == 1) {
            tx_leds_targets_pending[i] = tx_leds_targets_pending[i] - 1;
          }
        }
      }
    }
    if (tx_led_change) {
      rgb_leds[tx_leds_coords[tx_led_id_prev][0]][tx_leds_coords[tx_led_id_prev][1]].setIR(0);
      tx_led_change = false;
    }
    if (tx_active) {
      if (tx_half_cycle == 1) {
        tx_bit_pos = (tx_bit_pos + 1) % TX_BITS_COUNT;
        if ((--(tx_leds_targets_pending[tx_led_id])) == 0) {
          tx_led_id_prev = tx_led_id;
          tx_led_change = true;
          if ((++tx_led_id) == tx_leds_count) {
            tx_active = false;
          }
        }
      }
    }
    if (tx_reset) {
      tx_active = true;
      tx_led_id = 0;
      tx_led_id_prev = 255;
      tx_slot_id = 0;
      memcpy(tx_leds_targets_pending, tx_leds_targets, 16);
      tx_half_cycle = 0;
      led_drivers[0].setSingleRegister(0x40, 0); //I All
      led_drivers[1].setSingleRegister(0x40, 0); //I All
      tx_reset = false;
    }
    else {    
      tx_half_cycle = 1 - tx_half_cycle;
      if (tx_half_cycle == 0) {
        tx_slot_id = (tx_slot_id + 1)%TX_MAX_SLOTS;
        if (tx_slot_id == 0) {
          tx_reset = true;
          tx_active = false;
          tx_led_change = false;
        }      
      }
    }
    tx_led_I = 255 * ((~(tx_bits[tx_bit_pos] ^ tx_half_cycle)) & 0x01);
    
    tx_tick = false;
  }
  if (Serial.available() < 2) {
    return;
  }
  if (Serial.read() != CMD_STT) {
    return;
  }
  char c = Serial.read();
  if (c == 'b') {
    //Blink
    Timer3.detachInterrupt(); // Disconnects handler and stops timer
    led_drivers[0].setSingleRegister(0x40, 0); //I All
    led_drivers[1].setSingleRegister(0x40, 0); //I All
    
    tx_leds_count = Serial.parseInt();
    for (uint8_t i=0; i<tx_leds_count; i++) {
      tx_leds_coords[i][0] = Serial.parseInt();
      tx_leds_coords[i][1] = Serial.parseInt();
      tx_leds_targets[i] = Serial.parseInt();
    }

    long us = Serial.parseInt();

    if (tx_leds_count != 0) {
      memcpy(tx_leds_targets_pending, tx_leds_targets, 16);
      tx_reset = true;
      tx_active = false;
      tx_led_change = false;
      Timer3.attachInterrupt(handler_tx);
      Timer3.start(us);
    }
  }
  else if (c == 's') {
    //Sample

    Timer3.detachInterrupt(); // Disconnects handler and stops timer
    led_drivers[0].setSingleRegister(0x40, 0); //I All
    led_drivers[1].setSingleRegister(0x40, 0); //I All

    uint8_t i = Serial.parseInt();
    uint8_t j = Serial.parseInt();

    uint16_t samp_count = 0;
    end_sampling = false;

    Timer3.attachInterrupt(handler_end_sampling);
    Timer3.start(BURST_TM_US);
  
    do {
      adc_samps[samp_count].t = micros();
      adc_samps[samp_count].v = rgb_leds[i][j].getADCR() - led_r_rx_ambs[i][j];
    } while ((++samp_count < MAX_SAMPLES) && (end_sampling == false));  
    
    Timer3.detachInterrupt(); // Disconnects handler and stops timer
  
    Serial.print("Samples Count: ");
    Serial.println(samp_count);
    Serial.println("*"); 
    for (uint16_t i=0; i<samp_count; i++) {
      Serial.print(adc_samps[i].t);
      Serial.print(",");
      Serial.println(adc_samps[i].v);
    }
    Serial.println("#");
  }
}
