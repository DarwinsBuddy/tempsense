import random

from ..sensor import DS18B20


class MockedDS18B20(DS18B20):

    def __init__(self, count_devices=3, retries=5):
        super().__init__(retries=retries)
        self._count_devices = count_devices
        self._devices = [f'{self._mocked_name(i+1)}' for i in range(count_devices)]

    def _setup(self):
        pass

    @staticmethod
    def _mocked_name(i):
        return f"@Mock{i}"

    def device_name(self, i):
        return self._devices[i]

    def device_names(self):
        return self._devices

    def _read_temp(self, idx) -> float | None:
        return random.gauss(26, 5)

    def device_count(self):
        return self._count_devices
