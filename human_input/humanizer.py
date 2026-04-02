import random 

from human_input.protocol import HIDCommand as HID

class Humanizer: 
    def process_text(self, text):
        for char in text:
            char_code = ord(char)
            
            yield (HID.KEY_DOWN, char_code)
            yield (HID.WAIT, random.uniform(0.05, 0.15))
            yield (HID.KEY_UP, char_code)
            yield (HID.WAIT, random.uniform(0.08, 0.25))

        yield (HID.KEY_RELEASE_ALL, 0)
