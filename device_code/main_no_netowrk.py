from read_temp import TemperatureSensor
from OLED import OLED
from cooler import Cooler
from PID import PID
from Motor import PumpPWM, PumpStep
from RGB_LED import LED
from time_date import TimeAndDate
from Light_Sensor import LightSensor
from machine import Pin, Timer
from umqtt.robust import MQTTClient
import utime
import network
import time
import os

RUN = True

Pinbutton = Pin(39, Pin.IN)
lightSensor = LightSensor()
temperatureSensor = TemperatureSensor(32)
oledScreen = OLED(22, 23)
pumpAlgae = PumpStep(15, 33)
pumpCooler = PumpPWM(27, 12, 1)
cooler = Cooler(4, 5)
dateAndTime = TimeAndDate(2023, 6, 21, 2, 11, 40)
led = LED()
led.turn_on_led() # Turn on led

# PID controller and parameters
PID = PID(temperatureSensor.read_temp(), 17) # Terget temperature
PID.setProportional(8.5)
PID.setIntegral(3)
PID.setDerivative(0.5)

try:
    my_file = open('pid.txt') # Check if the file exists
except OSError:
    with open('pid.txt', 'w') as my_file:  # If not, create it in "write" mode
        my_file.write('Test of PID\n')


ACTIVATION_INTERVAL_PID = 10000 # 10s 
# ACTIVATION_INTERVAL_FOOD = 10000 # 10s
ACTIVATION_CONCENTRATION_MUSSEL = 10000*6*10 # 10 minutes


CLOCK_WISE_EMPTY_PUMP = 23
COUNTERCLOCK_WISE_EMPTY_PUMP = 26


mussel_number = 3
Concentration_mussel_bucket = mussel_number*1250
Concentration_mussel_bucket_at_time = 0
Volume_of_bucket = 4*1000 # mL

def RUN_TO_FALSE():
    global RUN
    RUN = False

def adjustSpeedCoolerPump(outputPID):
    if outputPID <= 2:
        cooler.LowPower()
        pumpCooler.set_speed(1)

    elif outputPID <= 12:
        cooler.HighPower()
        pumpCooler.set_speed(int(500*outputPID))
        time.sleep(0.4)
        pumpCooler.set_speed(int(1000*outputPID))

    else:
        cooler.fanOn()
        cooler.HighPower()
        pumpCooler.set_speed(7000)
        time.sleep(0.4)
        pumpCooler.set_speed(14000)

def read_temperature(temperatureSensor):
    temperatures = [] 
    i = 10 # Samples to average on (Note: read_temp() already averages over 50 readings)
    for _ in range(i):
        temperatures.append(temperatureSensor.read_temp())
    newTemp = sum(temperatures)/i - 1 # Temperature sensor off-set compensation
    return newTemp

        
# Run the first activation and start timer
initalTemperature = temperatureSensor.read_temp()
initalActuatorValue = PID.update(initalTemperature)
adjustSpeedCoolerPump(initalActuatorValue)
timeActivationPump = utime.ticks_ms()

# Run the first feed and start timer
mLOfFood = -Volume_of_bucket*(Concentration_mussel_bucket_at_time - Concentration_mussel_bucket)/(lightSensor.computeConc(lightSensor.computeOD()) - Concentration_mussel_bucket)
cycles_clockwise = mLOfFood/0.3155 + CLOCK_WISE_EMPTY_PUMP # Feed the mussel
cycles_couterclockwise =  mLOfFood/0.2868 + COUNTERCLOCK_WISE_EMPTY_PUMP # Feed the algae

print("\nMussels fed with: " + str(cycles_clockwise*3200))
print("mL: " + str(mLOfFood))
pumpAlgae.direction_clockwise()
pumpAlgae.cycle(cycles_clockwise*3200)
timeActivationFood = utime.ticks_ms()


while RUN == True:
    newTemp = read_temperature(temperatureSensor)

    # PID controller
    actuatorValue = PID.update(newTemp)

    if utime.ticks_diff(utime.ticks_ms(), timeActivationPump) >= ACTIVATION_INTERVAL_PID:
        adjustSpeedCoolerPump(actuatorValue)
        timeActivationPump = utime.ticks_ms()
        print("\n\nActuator:" + str(actuatorValue))
        print("Avg Temperature:" + str(newTemp))
        print("Time:" + str(dateAndTime.date_time()))
        print("PID Values:" + PID.overviewParameters)
        print("Frequency cooler pump: " + str(pumpCooler.step.freq()))
        print("Light intensity: " + str(lightSensor.readIntensity()))

        pump1 = pumpCooler.step.freq()
        # pump2 = pumpAlgae.step.freq()
        lightIntensity = lightSensor.readIntensity()
        ODValue = lightSensor.computeOD()
        concentration = lightSensor.computeConc(ODValue)
        
        # Write to file
        with open("pid.txt", "a") as my_file:
            my_file.write(dateAndTime.date_time()+ ", " + str(newTemp)+ ", " + str(pump1) + ", " + str(concentration) + ", " + str(lightIntensity) + "\n")
            my_file.close()

        # Update the oled screen
        oledScreen.display_PID_controls(newTemp, concentration, pump1, dateAndTime.date_time())

    if (utime.ticks_diff(utime.ticks_ms(), timeActivationFood) >= ACTIVATION_CONCENTRATION_MUSSEL):
        print("\nAlgae fed with: " + str(cycles_couterclockwise*3200))
        print("mL: " + str(mLOfFood))
        pumpAlgae.direction_counterclockwise()
        pumpAlgae.cycle(cycles_couterclockwise*3200)
        
        Concentration_mussel_bucket_at_time = 750
        
        mLOfFood = -Volume_of_bucket*(Concentration_mussel_bucket_at_time - Concentration_mussel_bucket)/(lightSensor.computeConc(lightSensor.computeOD()) - Concentration_mussel_bucket)
        cycles_clockwise = mLOfFood/0.3155 + CLOCK_WISE_EMPTY_PUMP # Feed the mussel
        cycles_couterclockwise =  mLOfFood/0.2868 + COUNTERCLOCK_WISE_EMPTY_PUMP # Feed the algae
        
        print("\nAlgae fed with: " + str(cycles_clockwise*3200))
        print("mL: " + str(mLOfFood))
        pumpAlgae.direction_clockwise()
        pumpAlgae.cycle(cycles_clockwise*3200)
        
        timeActivationFood = utime.ticks_ms()

    if Pinbutton.value() == 1:
        RUN_TO_FALSE()
        break

# Turn off system
pumpCooler.set_speed(1)
cooler.fanOff()