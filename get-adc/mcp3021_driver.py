import smbus
import time

class MCP3021:
    def __init__(self, dynamic_range, verbose = False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.adress = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_word_data(self.adress, 0)
        lower_byte = data >> 8
        upper_byte = data & 0xFF
        number = (upper_byte << 6) | (lower_byte >> 2)
        if self.verbose:
            print(f"Принятые данные: {data}, Страший байт: {upper_byte:x}, Младший байт: {lower_byte:x}, Число: {number}")
        return number
    
    def get_voltage(self):
        return self.get_number() / 1024 * self.dynamic_range
    
if __name__ == "__main__":
    try:
        mcp = MCP3021(5.2, 1)
        while True:
            print(mcp.get_voltage())
            time.spleep(1)
    finally:
        mcp.deinit()
