#include <Keyboard.h>

#define SoF             0xAA
#define ACK             0x06
#define READY           0x10
#define CMD_KEY_DOWN    0x21
#define CMD_KEY_UP      0x22
#define CMD_RELEASE_ALL 0x23
#define CMD_PING        0x7E

enum RxState {
  WAIT_SOF,
  WAIT_CMD,
  WAIT_KEY
};

RxState rxState = WAIT_SOF;
byte rxCmd = 0;
byte rxKey = 0;

void setup() {
  Serial.begin(115200);
  Keyboard.begin();
  while (!Serial) {}
  Serial.write(READY);
}

void loop() {
  while (Serial.available() > 0) {
    byte b = Serial.read();

    switch (rxState) {
      case WAIT_SOF:
        if (b == SoF) {
          rxState = WAIT_CMD;
        } 
        break;

      case WAIT_CMD:
        rxCmd = b;
        rxState = WAIT_KEY;
        break;

      case WAIT_KEY:
        rxKey = b;

        executeCommand(rxCmd, rxKey);
        Serial.write(ACK);

        rxState = WAIT_SOF;
        break;
    }
  }
}

void executeCommand(byte cmd, byte key) {
  switch (cmd) {
    case CMD_PING:
      break;

    case CMD_KEY_DOWN:
      Keyboard.press(key);
      break;

    case CMD_KEY_UP:
      Keyboard.release(key);
      break;

    case CMD_RELEASE_ALL:
      Keyboard.releaseAll();
      break;

    default:
      break;
  }
}