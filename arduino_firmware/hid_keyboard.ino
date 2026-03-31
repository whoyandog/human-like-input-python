#include <Keyboard.h>

#define READY           0x01
#define HEADER          0x02
#define CMD_PRESS       0x11
#define CMD_RELEASE     0x12
#define CMD_RELEASE_ALL 0x13
#define ACK             0x06 

void setup() {
  Serial.begin(115200);
  Keyboard.begin();
  
  while (!Serial);
  Serial.write(READY);
}

void loop() {
  if (Serial.available() >= 3) {
    if (Serial.peek() == HEADER) {
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
    case CMD_PRESS:
      Keyboard.print("1");  

      Keyboard.press(key);
      break;
      
    case CMD_RELEASE:
      Keyboard.print("2");

      Keyboard.release(key);
      break;

    case CMD_RELEASE_ALL:
      Keyboard.print("3");

      Keyboard.releaseAll();
      break;
  }
}