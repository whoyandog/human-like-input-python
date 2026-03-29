import serial
import serial.tools.list_ports as list_ports
import time


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
            time.sleep(2)
        except serial.SerialException as e:
            raise ConnectionError(f"Ошибка подключения к порту {port}: {e}")
        except Exception as e:
            raise ConnectionError(f"Непредвиденная ошибка при подключении к порту {port}: {e}")

    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def write(self, data):
        if not self.is_connected():
            self.connect()
        
        if isinstance(data, str):
            data = data.encode()
        
        self.ser.write(data)

    def disconnect(self):
        if self.is_connected():
            self.ser.close()
