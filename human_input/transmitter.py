import serial
import serial.tools.list_ports as list_ports
import struct

from human_input.protocol import HIDCommand as HID

class Transmitter:
    def __init__(self, cfg_settings):
        self.cfg_settings = cfg_settings
        self.ser = None

    def _find_atmega_port(self):
        ports = list_ports.comports()
        for port in ports:
            for target in self.cfg_settings.hardware["target_devices"]:
                if port.vid == target["vid"] and port.pid == target["pid"]:
                    return port.device
        return None
    
    def _send_packet(self, cmd, key=0x00):
        packet = struct.pack('BBB', HID.SoF, cmd, key)
        self.ser.write(packet)
        self.ser.flush()

    def _wait_ack(self, attempts):
        for i in range(1, attempts + 1):
            self._send_packet(HID.PING)
            response = self.ser.read(1)

            if response:
                b = response[0]
                if b == HID.ACK:
                    return True
            else:
                print(f"PING попытка {i}: таймаут")

        return False
    
    def _is_connected(self):
        return self.ser is not None and self.ser.is_open

    def connect(self):
        port = self._find_atmega_port()
        if not port:
            raise ValueError("ATmega устройство не подключено")
        
        try:
            self.ser = serial.Serial(
                port, 
                self.cfg_settings.hardware["baudrate"], 
                timeout=self.cfg_settings.hardware["handshake_timeout"]
            )

            if not self._wait_ack(self.cfg_settings.hardware["handshake_attempts"]):
                self.ser.close()
                self.ser = None
                raise ConnectionError(f"Превышено время ожидания Handshake: не получен ACK после {self.cfg_settings.hardware['handshake_attempts']} попыток")

            self.ser.reset_input_buffer()
            self.ser.timeout = self.cfg_settings.hardware["command_timeout"]
        except serial.SerialException as e:
            raise ConnectionError(f"Ошибка подключения к порту {port}: {e}")

    def send_cmd(self, cmd, key):
        if not self._is_connected():
            self.connect()
        
        try: 
            self._send_packet(cmd, key)
            response = self.ser.read(1)

            if response and response[0] == HID.ACK:
                return True
            
            return False
        
        except (serial.SerialException, OSError) as e:
            print(f"Ошибка Serial: {e}")
            return False
        
    def disconnect(self):
        if self._is_connected():
            self.ser.close()
            self.ser = None