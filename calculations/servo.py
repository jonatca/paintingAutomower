import smbus
import time

# PCA9685 Registers
MODE1 = 0x00
MODE2 = 0x01
SUBADR1 = 0x02
SUBADR2 = 0x03
SUBADR3 = 0x04
PRESCALE = 0xFE
LED0_ON_L = 0x06
LED0_ON_H = 0x07
LED0_OFF_L = 0x08
LED0_OFF_H = 0x09
ALL_LED_ON_L = 0xFA
ALL_LED_ON_H = 0xFB
ALL_LED_OFF_L = 0xFC
ALL_LED_OFF_H = 0xFD

# Set the I2C address of the PCA9685
pca9685_address = 0x7F

# Set the frequency of the PWM signal (in Hz)
frequency = 50

# Initialize the I2C bus
bus = smbus.SMBus(0)

# Reset PCA9685
bus.write_byte_data(pca9685_address, MODE1, 0x00)

# Set frequency
prescale_val = int(25e6 / (4096 * frequency) - 1)
old_mode = bus.read_byte_data(pca9685_address, MODE1)
new_mode = (old_mode & 0x7F) | 0x10
bus.write_byte_data(pca9685_address, MODE1, new_mode)
bus.write_byte_data(pca9685_address, PRESCALE, prescale_val)
bus.write_byte_data(pca9685_address, MODE1, old_mode)
time.sleep(0.005)
bus.write_byte_data(pca9685_address, MODE1, old_mode | 0x80)

# Set pulse range (in microseconds)
pulse_min = 1000
pulse_max = 2000

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000 / frequency
    pulse_length /= 4096
    pulse *= 1000
    pulse /= pulse_length
    on_time = 0
    off_time = int(pulse)
    bus.write_byte_data(pca9685_address, LED0_ON_L + 4 * channel, on_time & 0xFF)
    bus.write_byte_data(pca9685_address, LED0_ON_H + 4 * channel, on_time >> 8)
    bus.write_byte_data(pca9685_address, LED0_OFF_L + 4 * channel, off_time & 0xFF)
    bus.write_byte_data(pca9685_address, LED0_OFF_H + 4 * channel, off_time >> 8)

# Set servo position
def set_servo_position(channel, angle):
    pulse_range = pulse_max - pulse_min
    pulse = int(pulse_min + (angle / 180.0) * pulse_range)
    set_servo_pulse(channel, pulse)


