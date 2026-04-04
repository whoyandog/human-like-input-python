from enum import IntEnum

class AppCommand(IntEnum):
    WAIT = 0x01

class HIDCommand(IntEnum):
    SoF = 0xAA
    PING = 0x7E
    ACK = 0x06
    KEY_DOWN = 0x21
    KEY_UP = 0x22
    KEY_RELEASE_ALL = 0x23


class HIDKey(IntEnum):
    LEFT_SHIFT = 0x81
    BACKSPACE = 0xB2

