#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>

void setup(){
    Serial.begin(9600);
    SPI.begin();
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop(){
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
    digitalWrite(LED_BUILTIN, HIGH);;
    delay(1000);
    Serial.println("A");
}
