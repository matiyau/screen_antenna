#include <Arduino.h>

void setup() {
    Serial.begin(115200);

#ifdef MAT_BIG
    Serial.println("Big");
#else
    Serial.println("Small");
#endif
}

void loop() {
// write your code here
}