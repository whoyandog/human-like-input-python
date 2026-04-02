#include <Keyboard.h>

#define SoF             0xAD // start of frame
#define ACK             0x06 
#define READY           0x10
#define CMD_KEY_DOWN    0x21
#define CMD_KEY_UP      0x22
#define CMD_RELEASE_ALL 0x23

void setup() {
  Serial.begin(115200);
  Keyboard.begin();
  
  while (!Serial);
  Serial.write(READY);
}

void loop() {
  while (Serial.available() > 0 && Serial.peek() != SoF) {
    Serial.read();
  }

  if (Serial.available() >= 3) {
    if (Serial.peek() == SoF) {
      Serial.read();
      Keyboard.print("+");
      
      byte cmd = Serial.read();  
      byte key = Serial.read(); 

      if (key == 108) {
        return;
      }

      executeCommand(cmd, key);

      Serial.write(ACK);
    } else {
      Serial.read();
      Keyboard.print("-");
    }
  }
}

void executeCommand(byte cmd, byte key) {
  switch (cmd) {
    case CMD_KEY_DOWN:
      Keyboard.print("1");  

      Keyboard.press(key);
      break;
      
    case CMD_KEY_UP:
      Keyboard.print("2");

      Keyboard.release(key);
      break;

    case CMD_RELEASE_ALL:
      Keyboard.print("3");

      Keyboard.releaseAll();
      break;
  }
}