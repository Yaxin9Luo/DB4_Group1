from machine import Pin, PWM, I2C
from time import sleep
# Pin definitions
motor1pin1 = Pin(21, Pin.OUT)
motor1pin2 = Pin(17, Pin.OUT)
motor2pin1 = Pin(27, Pin.OUT)
motor2pin2 = Pin(33, Pin.OUT)

ena_pin = PWM(Pin(32), freq=1000)
enb_pin = PWM(Pin(12), freq=1000)

# Function to set motor speed
def set_speed(pwm, duty_cycle):
    pwm.duty(duty_cycle)

# Function to set motor direction
def set_direction(motor_pin1, motor_pin2, direction):
    if direction == "forward":
        motor_pin1.value(0)
        motor_pin2.value(1)
    elif direction == "backward":
        motor_pin1.value(0)
        motor_pin2.value(1)