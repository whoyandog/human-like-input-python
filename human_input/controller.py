import time

from human_input.config import settings
from human_input import transmitter
from human_input import humanizer
from human_input.protocol import HIDCommand as HID


class HumanLikeInput:
    def __init__(self):
        self.tx = transmitter.Transmitter(settings)
        self.humanizer = humanizer.Humanizer()
        self.history = []
    
    def connect(self):
        self.tx.connect()

    def disconnect(self):
        self.tx.disconnect()
    
    def type_text(self, text):
        # Временно закомменировать для теста
        #  
        # for cmd, key in self.humanizer.process_text(text):
        #     if cmd == HID.WAIT:
        #         time.sleep(key)
        #     else: 
        #         success = self.tx.send_cmd(cmd, key)

        #         if success: 
        #             if cmd == HID.KEY_DOWN:
        #                 self.history.append(key)
                
        #         else: H
        #             print(f"Символ {chr(key)} не был отправлен!")

        self.tx.send_cmd(HID.KEY_DOWN, ord('h'))
        self.tx.send_cmd(HID.KEY_UP, ord('h'))
        self.tx.send_cmd_no_header(HID.KEY_RELEASE_ALL, 0)

        print("Отправленный текст: " + ''.join(chr(k) for k in self.history))

    
            

    

