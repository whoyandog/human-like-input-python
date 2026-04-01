import serial
import serial.tools.list_ports as list_ports
import struct

import time # удалить

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

            start_open = time.perf_counter() # удалить

            self.ser = serial.Serial(
                port, 
                self.cfg_settings.hardware["baudrate"], 
                timeout=self.cfg_settings.hardware["timeout"]
            )

            end_open = time.perf_counter() # delete
            print(f"Порт открыт за: {end_open - start_open:.4f} сек") # delete
 
            print("Ожидаю сигнал готовности от устройства...")


            start_read = time.perf_counter()

            ready_signal = self.ser.read(1)

            end_read = time.perf_counter()
            delta_read = end_read - start_read
            print(f"Ответ получен за: {delta_read:.4f} сек")

            for byte in ready_signal:
                print(f"Получен байт: {byte}")

            if ready_signal and ready_signal[0] == HID.READY:
                print("Устройство готово")
            else:
                print("Сигнал не получен")
            
            self.ser.reset_input_buffer()

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
            start_send = time.perf_counter()

            self.ser.reset_input_buffer()
            self.ser.write(packet)
            self.ser.flush()

            response = self.ser.read(1)

            end_send = time.perf_counter()
            delta_read = end_send - start_send
            print(f"Отправки завершена за: {delta_read:.4f} сек")

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
            start_send = time.perf_counter()

            self.ser.reset_input_buffer()
            self.ser.write(packet)
            self.ser.flush()

            response = self.ser.read(1)

            end_send = time.perf_counter()
            delta_read = end_send - start_send
            print(f"Отправки завершена за: {delta_read:.4f} сек")

            if response and response[0] == HID.ACK:
                print("Команда успешно отправлена и подтверждена!")
                return True
            
            print("Ответ не получен или не является ACK!")
            return False
        
        except Exception as e:
            print(f"Ошибка Serial: {e}")
            return False

    def disconnect(self):
        print("попытка закрыть порт")
        if self.is_connected():
            print("закрытие порта")
            self.ser.close()
