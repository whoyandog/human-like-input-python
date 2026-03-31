from enum import IntEnum

class HIDCommand(IntEnum):
    WAIT = 0x00
    READY = 0x01
    HEADER = 0x02
    KEY_PRESS = 0x11
    KEY_RELEASE = 0x12
    KEY_RELEASE_ALL = 0x13
    ACK = 0x06
