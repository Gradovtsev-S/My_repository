import RPi.GPIO as gp

gp.setmode(gp.BCM)

dac_bits = [16, 20, 21, 25, 26, 17, 27, 22]
gp.setup(dac_bits, gp.OUT)

dynamic_range = 3.3

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f'Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)')
        print(f'Устанавливаем 0.0 В')
        return 0
    
    return int(voltage / dynamic_range * 255)

def number_to_dac(number):
    bin_n = [int(element) for element in bin(number)[2:].zfill(8)]
    for i in range(len(dac_bits)):
        gp.output(dac_bits[i], bin_n[i])
    print(f"Число на вход ЦАП: {number}, {bin_n}")

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)
        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")
finally:
    gp.output(dac_bits, 0)
    gp.cleanup()
