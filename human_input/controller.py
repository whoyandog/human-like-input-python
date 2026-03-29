import random

from human_input.config import settings
from human_input import transmitter


class HumanLikeInput:
    def __init__(self):
        self.tx = transmitter.Transmitter(settings)
    
    def connect(self):
        self.tx.connect()

    def disconnect(self):
        self.tx.disconnect()
    
    def type_text(self, text):
        for char in text:
            hold_time = random.uniform(100, 300)  
            print ("hold time is: " + str(hold_time))

            char_code = ord(char)
        
            command = f"{char_code},{hold_time}\n"
            self.tx.write(command)
    

