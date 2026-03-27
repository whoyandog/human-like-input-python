#include <Keyboard.h>

void setup() {
  Serial.begin(9600); 
  Keyboard.begin();
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    int commaIndex = data.indexOf(',');
    if (commaIndex != -1) {
      int charCode = data.substring(0, commaIndex).toInt();
      int holdTime = data.substring(commaIndex + 1).toInt();

      Keyboard.press((char)charCode);
      delay(holdTime);
      Keyboard.releaseAll();
    }
  }
}