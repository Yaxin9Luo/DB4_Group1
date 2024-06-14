from i2c_test import *    
from read_temp import *
import time
import ssd1306
import tcs34725
from motors import *
# Pin definitions
motor1pin1 = Pin(21, Pin.OUT)
motor1pin2 = Pin(17, Pin.OUT)
motor2pin1 = Pin(27, Pin.OUT)
motor2pin2 = Pin(33, Pin.OUT)
ena_pin = PWM(Pin(32), freq=1000)
enb_pin = PWM(Pin(12), freq=1000)
try:
    while True:
        # Controlling speed (0 = off and 1023 = max speed):
        set_speed(ena_pin, 225)  # ENA pin (approx. 39% of 1023)
        set_speed(enb_pin, 225)  # ENB pin (approx. 78% of 1023)
        print("hello Kamran Oscar and Patrick")
        # Controlling spin direction of motors:
        set_direction(motor1pin1, motor1pin2, "forward")
        set_direction(motor2pin1, motor2pin2, "forward")
        time.sleep(10)
except KeyboardInterrupt:
    pass

