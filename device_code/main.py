from machine import Pin, PWM, I2C
import time



import ssd1306
import tcs34725

# Define I2C
i2c = I2C(scl=Pin(22), sda=Pin(23), freq=100000)

# Define olef
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)

# Define rgb sensor
sensor = tcs34725.TCS34725(i2c)
#sensor.integration_time(10) #value between 2.4 and 614.4.
#sensor.gain(16) #must be a value of 1, 4, 16, 60

def color_rgb_bytes(color_raw):
    #Read the RGB color detected by the sensor.  Returns a 3-tuple of
    #red, green, blue component values as bytes (0-255).
    #NOTE: These values are normalized against 'clear', remove the division
    #by 'clear' if you need the raw values.
    
    r, g, b, clear = color_raw
    # Avoid divide by zero errors ... if clear = 0 return black
    if clear == 0:
        return (0, 0, 0)
    red   = int(pow((int((r/clear) * 256) / 255), 2.5) * 255)
    green = int(pow((int((g/clear) * 256) / 255), 2.5) * 255)
    blue  = int(pow((int((b/clear) * 256) / 255), 2.5) * 255)
    # Handle possible 8-bit overflow
    if red > 255:
        red = 255
    if green > 255:
        green = 255
    if blue > 255:
        blue = 255
    return (red, green, blue)

    
fan = Pin(26, Pin.OUT)
cooler = PWM(Pin(25), freq=1000)


"""
def cooler_duty_cycle(pwm, duty_cycle):
    pwm.duty(duty_cycle)
    
def fan_on_off(fan,state):
    if state = "on":
        fan.value(1)
    elif state = "off"
        fan.value(0)
"""

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

try:
    while True:
        # Controlling speed (0 = off and 1023 = max speed):
        set_speed(ena_pin, 225)  # ENA pin (approx. 39% of 1023)
        set_speed(enb_pin, 225)  # ENB pin (approx. 78% of 1023)
        print("hello Bish and Alice and Emrah")

        # Controlling spin direction of motors:
        set_direction(motor1pin1, motor1pin2, "forward")
        set_direction(motor2pin1, motor2pin2, "forward")
        time.sleep(10)

        
        

        # Read color sensor
        r,g,b = color_rgb_bytes(sensor.read(True))

        # Show results on OLED
        oled.fill(0)
        oled.text('R: {}'.format(r), 0, 8)
        oled.text('G: {}'.format(g), 0, 16)
        oled.text('B: {}'.format(b), 0, 24)
        oled.show()

        # Print results
        answer = '>r:{} g:{} b:{}<'.format(r, g, b)
        print(answer, end='\n')

        # Wait 1 second before repeating
        time.sleep(10)

except KeyboardInterrupt:
    pass

# Cleanup
ena_pin.deinit()
enb_pin.deinit()