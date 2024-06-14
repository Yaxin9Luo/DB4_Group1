# The MIT License (MIT)
# Copyright (c) 2019 Mike Teachman
# https://opensource.org/licenses/MIT
#
# Example MicroPython and CircuitPython code showing how to use the MQTT protocol with Adafruit IO, to  
# publish and subscribe on the same device
#
# Tested using the releases:
#   ESP8266
#       MicroPython 1.9.3
#       MicroPython 1.9.4
#       MicroPython 1.10
#       CircuitPython 2.3.1     (needs addition of CircuitPython specific umqtt module)
#       CircuitPython 3.0.0     (needs addition of CircuitPython specific umqtt module)
#   ESP32
#       MicroPython 1.9.4       (needs addition of MicroPython umqtt module)
#       MicroPython 1.10
#
# Tested using the following boards:
#   Adafruit Feather HUZZAH ESP8266
#   Adafruit Feather HUZZAH ESP32
#   WeMos D1 Mini
#
# User configuration parameters are indicated with "ENTER_".
# Made by Yaxin Luo aka DavidTheCrazy and Antoine Ohn aka 
from device_code.i2c_test import *    
from device_code.read_temp import *
import time
import ssd1306
import tcs34725
from device_code.motors import *
import network
import time
from umqtt.robust import MQTTClient
import os
import gc
import sys

# the following function is the callback which is 
# called when subscribed data is received
def cb(topic, msg):
    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))
    command = str(msg, 'utf-8')
    
    if command.startswith('speed:'):
        speed = int(command.split(':')[1])
        global motor_speed
        motor_speed = speed
        set_speed(ena_pin, motor_speed)
        set_speed(enb_pin, motor_speed)
    elif command.startswith('direction:'):
        direction = command.split(':')[1]
        global motor_direction
        motor_direction = direction
        set_direction(motor1pin1, motor1pin2, motor_direction)
        set_direction(motor2pin1, motor2pin2, motor_direction)
    else:
        print('Unknown command')

# WiFi connection information
WIFI_SSID = 'Yaxin Luo'
WIFI_PASSWORD = '999999999'

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()

# create a random MQTT clientID 
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

# connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
# 
# To use a secure connection (encrypted) with TLS: 
#   set MQTTClient initializer parameter to "ssl=True"
#   Caveat: a secure connection uses about 9k bytes of the heap
#         (about 1/4 of the micropython heap on the ESP8266 platform)
ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'<ENTER_ADAFRUIT_USERNAME>'
ADAFRUIT_IO_KEY = b'<ENTER_ADAFRUIT_IO_KEY>'
ADAFRUIT_IO_FEEDNAME = b'freeHeap'

client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
                    
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    client.disconnect()
    print("\nDisconnected from the server, activities will run locally\n")
    # sys.exit()

# publish free heap statistics to Adafruit IO using MQTT
# subscribe to the same feed
#
# format of feed name:  
#   "ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME"
mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')
client.set_callback(cb)      
client.subscribe(mqtt_feedname) 
############## motor control ####################
# Pin definitions for motors
motor1pin1 = Pin(21, Pin.OUT)
motor1pin2 = Pin(17, Pin.OUT)
motor2pin1 = Pin(27, Pin.OUT)
motor2pin2 = Pin(33, Pin.OUT)
ena_pin = PWM(Pin(32), freq=1000)
enb_pin = PWM(Pin(12), freq=1000)   

# Initialize motor state
motor_speed = 225  # Default speed
motor_direction = "forward"  # Default direction
set_speed(ena_pin, motor_speed)
set_speed(enb_pin, motor_speed)
set_direction(motor1pin1, motor1pin2, motor_direction)
set_direction(motor2pin1, motor2pin2, motor_direction)
PUBLISH_PERIOD_IN_SEC = 10 
SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5 
accum_time = 0
while True:
    try:
        # Publish
        if accum_time >= PUBLISH_PERIOD_IN_SEC:
            free_heap_in_bytes = gc.mem_free()
            print('Publish:  freeHeap = {}'.format(free_heap_in_bytes))
            client.publish(mqtt_feedname,    
                           bytes(str(free_heap_in_bytes), 'utf-8'), 
                           qos=0) 
            accum_time = 0                
        
        # Subscribe.  Non-blocking check for a new message.  
        client.check_msg()
        # Ensure motors keep running with the last set speed and direction
        set_speed(ena_pin, motor_speed)
        set_speed(enb_pin, motor_speed)
        set_direction(motor1pin1, motor1pin2, motor_direction)
        set_direction(motor2pin1, motor2pin2, motor_direction)
        time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
        accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()