import random

from ..sensor import DS18B20


class MockedDS18B20(DS18B20):

    def __init__(self, device_map=None, count_devices=3, retries=5):
        super().__init__(retries=retries)
        if device_map is None:
            self.device_map = dict()
        else:
            self.device_map = device_map
        self._count_devices = count_devices
        self._devices = [f'{self._mocked_name(i+1)}' for i in range(count_devices)]

    def _setup(self):
        pass

    def _map_device_name(self, name):
        return self.device_map[name] if name in self.device_map else name

    def _map_device_names(self, names):
        return [self._map_device_name(n) for n in names]

    @staticmethod
    def _mocked_name(i):
        return f"@Mock{i}"

    def device_name(self, i):
        return self._map_device_name(self._devices[i])

    def device_names(self):
        return self._map_device_names(self._devices)

    def _read_temp(self, idx) -> float | None:
        return random.gauss(26, 5)

    def device_count(self):
        return self._count_devices
