import os
import glob
import time


class DS18B20:

    def _setup(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')
        self._count_devices = len(device_folder)
        self._devices = list()
        i = 0
        while i < self._count_devices:
            self._devices.append(device_folder[i] + '/w1_slave')
            i += 1

    def __init__(self, retries=5):
        self.retries = retries
        self._setup()

    def device_names(self):
        names = list()
        for i in range(self._count_devices):
            names.append(self._devices[i])
            temp = names[i][20:35]
            names[i] = temp
        return names

    # (one tab)
    def _read_temp(self, index):
        f = open(self._devices[index], 'r')
        raw_temp_lines = f.readlines()
        f.close()
        return raw_temp_lines

    @staticmethod
    def _parse_temp(raw_temp_lines):
        equals_pos = raw_temp_lines[1].find('t=')
        if equals_pos != -1:
            temp = raw_temp_lines[1][equals_pos + 2:]
            return float(temp) / 1000
        else:
            print("ERROR: could not read temperature: ", raw_temp_lines)
            return None

    def temp(self, index=0):
        raw_temp_lines = self._read_temp(index)
        retries = self.retries
        try:
            while (len(raw_temp_lines) > 0) and (raw_temp_lines[0].strip()[-3:] != 'YES') and (retries > 0):
                time.sleep(0.1)
                raw_temp_lines = self._read_temp(index)
                retries -= 1
            if retries == 0:
                print("ERROR: retries exceeded")
                return None

            return self._parse_temp(raw_temp_lines)
        except Exception as e:
            print("ERROR: ", e)
            return None
    
    def device_count(self):
        return self._count_devices
