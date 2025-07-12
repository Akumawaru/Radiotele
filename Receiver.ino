//upload this to arduino
#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 myADS;
int v;

void setup() {
  Serial.begin(115200);
  myADS.begin();
  myADS.setGain(GAIN_TWOTHIRDS);
}

void loop() {
  v = myADS.readADC_SingleEnded(0);
  Serial.println(v);
  delay(200);
}




