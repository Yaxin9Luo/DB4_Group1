from machine import Pin, PWM
import utime
class PumpPWM:
    def __init__(self, pinDirection, pinStep, speed) -> None:
        self.direction = Pin(pinDirection, Pin.OUT)
        self.step = PWM(Pin(pinStep), freq = speed, duty = 256)
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


class PumpStep:
    def __init__(self, pinDirection, pinStep) -> None:
        self.direction = Pin(pinDirection, Pin.OUT)
        self.step = Pin(pinStep, Pin.OUT)

    def oneStep(self):
        self.step.value(1-self.step.value())
    
    def direction_clockwise(self):
        self.direction.value(1)

    def direction_counterclockwise(self):
        self.direction.value(0)
  
    def cycle(self, stepsToPerform):
        # 3200 steps equals to one full rotation
        for i in range(stepsToPerform):
            self.oneStep()
            utime.sleep_us(10)
            self.oneStep()
            utime.sleep_us(10)
           # print(i)

    def intermittent_step(self, sleep):
        self.oneStep()
        utime.sleep_us(sleep)
        self.oneStep()
        utime.sleep_us(sleep)