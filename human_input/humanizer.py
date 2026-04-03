import random 

from human_input.protocol import HIDCommand as HC
from human_input.protocol import AppCommand as AC

class Humanizer: 
    def process_text(self, text):
        for char in text:
            char_code = ord(char)
            
            yield (HC.KEY_DOWN, char_code)
            yield (AC.WAIT, random.uniform(0.05, 0.15))
            yield (HC.KEY_UP, char_code)
            yield (AC.WAIT, random.uniform(0.08, 0.25))

        yield (HC.KEY_RELEASE_ALL, 0)
