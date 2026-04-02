from enum import IntEnum

class HIDCommand(IntEnum):
    WAIT = 0x00
    SoF = 0xAD
    READY = 0x10
    ACK = 0x06
    KEY_DOWN = 0x21
    KEY_UP = 0x22
    KEY_RELEASE_ALL = 0x23
