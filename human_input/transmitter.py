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
    
    def _send_ping(self):
        packet = struct.pack('BBB', HID.SoF, HID.PING, 0x00)
        self.ser.write(packet)
        self.ser.flush()

    def _wait_ready_or_ack(self, attempts=5):
        for i in range(1, attempts + 1):
            self._send_ping()
            response = self.ser.read(1)

            if response:
                b = response[0]
                print(f"PING попытка {i}: получен байт {b} (0x{b:02X})")
                if b == HID.READY:
                    print("Устройство готово (READY)")
                    return True
                if b == HID.ACK:
                    print("Устройство готово (ACK)")
                    return True
            else:
                print(f"PING попытка {i}: таймаут")

        return False

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

            normal_timeout = self.cfg_settings.hardware["timeout"]
            handshake_timeout = 0.02
            self.ser.timeout = handshake_timeout

            end_open = time.perf_counter() # delete
            print(f"Порт открыт за: {end_open - start_open:.4f} сек") # delete
 
            print("Ожидаю READY/ACK от устройства...")

            start_read = time.perf_counter()
            ready_signal = self.ser.read(1)
            end_read = time.perf_counter()
            delta_read = end_read - start_read
            print(f"Первое чтение завершено за: {delta_read:.4f} сек")

            handshake_ok = False
            if ready_signal:
                b = ready_signal[0]
                print(f"Первый байт: {b} (0x{b:02X})")
                if b == HID.READY:
                    print("Устройство готово (READY)")
                    handshake_ok = True
                elif b == HID.ACK:
                    print("Устройство готово (ACK)")
                    handshake_ok = True
                else:
                    print("Первый байт не READY/ACK, запускаю PING handshake")
                    handshake_ok = self._wait_ready_or_ack()
            else:
                print("READY не пришел на первом чтении, запускаю PING handshake")
                handshake_ok = self._wait_ready_or_ack()

            if not handshake_ok:
                print("Handshake не пройден")

            self.ser.timeout = normal_timeout

            # Показываем отладочный текст, который устройство могло отправить сразу после READY
            time.sleep(0.1)
            startup_tail = self.ser.read_all()
            if startup_tail:
                print(f"Стартовые байты (hex): {startup_tail.hex(' ')}")
                try:
                    print("Стартовый текст:", startup_tail.decode("utf-8", errors="replace").strip())
                except Exception:
                    pass
            
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
        packet = struct.pack('BBB', HID.SoF, cmd, key)
        print(f"TX: {packet.hex(' ')}")

        try: 
            start_send = time.perf_counter()

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
        
    
    def send_custom_cmd(self, data):
        if not self.is_connected():
            self.connect()

        print(f"Отправляю кастомную команду: {data}")
        if isinstance(data, (bytes, bytearray)):
            packet = bytes(data)
        else:
            try:
                packet = bytes(list(data))
            except TypeError:
                raise TypeError("data must be bytes or an iterable of integers 0-255")

        print(f"Сформированный пакет: {packet.hex(' ')}")

        try:
            start_send = time.perf_counter()

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
