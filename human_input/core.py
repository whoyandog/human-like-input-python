import serial
import time
import random

class HumanInputPrototype:
    def __init__(self, port, baudrate=9600):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)
        except Exception as e:
            raise

    def type_text(self, text):
        for char in text:
            hold_time = random.randint(70, 130)
            pause_between = random.uniform(0.08, 0.25)
            packet = f"{ord(char)},{hold_time}\n"
            self.ser.write(packet.encode())
            time.sleep(pause_between)

    def close(self):
        try:
            self.ser.close()
        except Exception:
            pass


def run_demo(port='COM5', text=None, delay=3):
    if text is None:
        text = "Hello, this is a human-like typing test."
    typist = HumanInputPrototype(port)
    print(f"Switch to target window in {delay} seconds...")
    time.sleep(delay)
    typist.type_text(text)
    typist.close()
