import time

from human_input.config import settings
from human_input import transmitter
from human_input import humanizer
from human_input.protocol import HIDCommand as HC
from human_input.protocol import AppCommand as AC



class HumanLikeInput:
    def __init__(self):
        self.tx = transmitter.Transmitter(settings)
        self.humanizer = humanizer.Humanizer(settings.typing_settings)
        self.history = []
    
    def connect(self):
        self.tx.connect()

    def disconnect(self):
        self.tx.disconnect()
    
    def type_text(self, text):
        sent_commands = 0
        for cmd, key in self.humanizer.process_text(text):
            if cmd == AC.WAIT:
                time.sleep(key)
            else: 
                success = self.tx.send_cmd(cmd, key)

                if success: 
                    if cmd == HC.KEY_DOWN:
                        sent_commands += 1
                
                else: 
                    print(f"Команда {int(cmd):#04x} с ключом {int(key):#04x} не была отправлена")

        print(f"Завершено: отправлено {sent_commands} нажатий")

    
            

    

