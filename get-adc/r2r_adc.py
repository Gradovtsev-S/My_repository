import RPi.GPIO as gp
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        gp.setmode(gp.BCM)
        gp.setup(self.bits_gpio, gp.OUT, initial = 0)
        gp.setup(self.comp_gpio, gp.IN)

    def deinit(self):
        gp.output(self.bits_gpio, 0)
        gp.cleanup()
    
    def number_to_dac(self, number):
        for i in range(len(self.bits_gpio)):
            gp.output(self.bits_gpio[i], [int(element) for element in bin(number)[2:].zfill(8)][i])

    def sequential_counting_adc(self):
        for digital_code in range(0, 255):
            self.number_to_dac(digital_code)
            time.sleep(self.compare_time)

            compare_state = gp.input(self.comp_gpio)

            if compare_state == 1:
                return max(0, digital_code - 1)
        return 255
    
    def get_sc_voltage(self):
        digital_value = self.sequential_counting_adc()
        return (digital_value / 255) * self.dynamic_range

    def successive_approximation_adc(self):
        low = 0
        high = 255

        while high - low > 1:
            mid = (low + high) // 2
            self.number_to_dac(mid)
            time.sleep(self.compare_time)

            if gp.input(self.comp_gpio) == gp.HIGH:
                high = mid
            else:
                low = mid
        
        return high
    
    def get_sar_voltage(self):
        return self.successive_approximation_adc() / 255 * self.dynamic_range
    
if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.3)

        while True:
            voltage = adc.get_sc_voltage()
            print(f'Измеренное напряжение: {voltage:.3f} В')
            print(adc.get_sar_voltage())

    finally:
        adc.deinit()