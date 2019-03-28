import time

class HTU21D(object):
    ADDRESS = 0x40
    ISSUE_TEMP_ADDRESS = b'\xF3'
    ISSUE_HU_ADDRESS = b'\xF5'

    def __init__(self, i2c):
        self.i2c = i2c
        if 64 not in i2c.scan():
            raise ValueError('Could not find the sensor on the i2c bus')


    def _crc_check(self, value):
        remainder = ((value[0] << 8) + value[1]) << 8
        remainder |= value[2]
        divsor = 0x988000

        for i in range(0, 16):
            if remainder & 1 << (23 - i):
                remainder ^= divsor
            divsor >>= 1

        if remainder == 0:
            return True
        else:
            return False

    def _issue_measurement(self, write_address):
        self.i2c.start()
        self.i2c.writeto(self.ADDRESS, write_address)
        time.sleep_ms(500) 
        data = self.i2c.readfrom(self.ADDRESS, 3)
        if not self._crc_check(data):
            raise ValueError()
        raw = (data[0] << 8) + data[1]
        raw &= 0xFFFC
        self.i2c.stop()
        return raw

    @property
    def temperature(self):
        return -46.85 + (175.72 * self._issue_measurement(self.ISSUE_TEMP_ADDRESS) / 65536)

    @property
    def humidity(self):
        return -6 + (125.0 * self._issue_measurement(self.ISSUE_HU_ADDRESS) / 65536)