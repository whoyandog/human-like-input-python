import serial
import serial.tools.list_ports as list_ports
import struct

import time

from human_input.protocol import HIDCommand as HID

class Transmitter:
    def __init__(self, cfg_settings):
        self.cfg_settings = cfg_settings
        self.ser = None

    def find_atmega_port(self):
        ports = list_ports.comports()
        for port in ports:
            for target in self.cfg_settings.hardware["target_devices"]:
                if port.vid == target["vid"] and port.pid == target["pid"]:
                    return port.device
        return None

    def connect(self):
        port = self.find_atmega_port()
        if not port:
            raise ValueError("Atmega port not found")
        
        try:
            self.ser = serial.Serial(
                port, 
                self.cfg_settings.hardware["baudrate"], 
                timeout=self.cfg_settings.hardware["timeout"]
            )

            print("Ожидаю сигнал готовности от устройства...")

            ready_signal = self.ser.read(1)

            for byte in ready_signal:
                print(f"Получен байт: {byte}")

            if ready_signal and ready_signal[0] == HID.READY:
                print("Устройство готово")
            else:
                print("Сигнал не получен")
            
            self.ser.reset_input_buffer

        except serial.SerialException as e:
            raise ConnectionError(f"Ошибка подключения к порту {port}: {e}")
        except Exception as e:
            raise ConnectionError(f"Непредвиденная ошибка при подключении к порту {port}: {e}")

    def is_connected(self):
        return self.ser is not None and self.ser.is_open
    
    def send_cmd(self, cmd, key):
        if not self.is_connected():
            self.connect()

        print(f"Отправляю команду: {cmd}, ключ: {key}")
        packet = struct.pack('BBB', HID.HEADER, cmd, key)

        try: 
            self.ser.reset_input_buffer()
            self.ser.write(packet)
            self.ser.flush()

            response = self.ser.read(1)

            if response and response[0] == HID.ACK:
                print("Команда успешно отправлена и подтверждена!")
                return True
            
            print("Ответ не получен или не является ACK!")
            return False
        
        except Exception as e:
            print(f"Ошибка Serial: {e}")
            return False
        
    def send_cmd_no_header(self, cmd, key):
        if not self.is_connected():
            self.connect()

        print(f"Отправляю команду: {cmd}, ключ: {key}")
        packet = struct.pack('BBB', HID.READY, cmd, key)

        try: 
            self.ser.reset_input_buffer()
            self.ser.write(packet)
            self.ser.flush()

            response = self.ser.read(1)

            if response and response[0] == HID.ACK:
                print("Команда успешно отправлена и подтверждена!")
                return True
            
            print("Ответ не получен или не является ACK!")
            return False
        
        except Exception as e:
            print(f"Ошибка Serial: {e}")
            return False

    def disconnect(self):
        if self.is_connected():
            self.ser.close()
