import os
import glob
import time
from typing import Optional


class SensorData:
    def __init__(self, device, temp_celsius):
        self.device = device
        self.temp_celsius = temp_celsius

    def get_temp(self, unit='c', decimal_places=3):
        if self.temp_celsius is not None:
            if unit == 'c':
                return round(self.temp_celsius, decimal_places)
            elif unit == 'f':
                return round(self.temp_celsius * 9.0 / 5.0 + 32, decimal_places)
            else:
                print(f"Unable to read temperature for sensor")
                return None

    def format_temp(self, unit='c'):
        t = self.get_temp(unit)
        return f'{t:.3f}' if t is not None else ''


class DS18B20:

    def _setup(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(self.base_dir + '28*')
        self._count_devices = len(device_folder)
        self._devices = list()
        self._devices = [device_folder[i] + '/w1_slave' for i in range(self._count_devices)]

    def __init__(self, retries=5):
        self.retries = retries
        self._setup()

    def device_name(self, i):
        return self._devices[i][len(self.base_dir):35]

    def device_names(self):
        return [self.device_name(i) for i in range(self._count_devices)]

    def _read_temp(self, idx) -> Optional[float]:
        f = open(self._devices[idx], 'r')
        raw_temp_lines = f.readlines()
        f.close()
        if len(raw_temp_lines) > 0 and (raw_temp_lines[0].strip()[-3:] == 'YES'):
            return self._parse_temp(raw_temp_lines)
        else:
            return None

    @staticmethod
    def _parse_temp(raw_temp_lines) -> Optional[float]:
        equals_pos = raw_temp_lines[1].find('t=')
        if equals_pos != -1:
            temp = raw_temp_lines[1][equals_pos + 2:]
            return float(temp) / 1000
        else:
            print("ERROR: could not read temperature: ", raw_temp_lines)
            return None

    def temp(self, index=0) -> Optional[SensorData]:
        retries = self.retries
        if index >= len(self._devices):
            print(f"ERROR: Unknown device with index={index} (count: {len(self._devices)}")
            return None
        dev_name = self.device_name(index)
        while True:
            try:
                temp_c = self._read_temp(index)
            except Exception as e:
                print("ERROR: ", e)
                temp_c = None
            if temp_c is not None:
                return SensorData(device=dev_name, temp_celsius=temp_c)
            if retries == 0:
                print("ERROR: retries exceeded")
                return SensorData(device=dev_name, temp_celsius=None)
            retries -= 1
            time.sleep(0.1)
    
    def device_count(self):
        return self._count_devices
