"""
# simple-gpio.py

    This is a simple GPIO program to test whether the hardware
    connection works as expected or not. It flashes the LED
    depending upon state of LightSensor, when dark the led
    should shine, when bright, it should turn off.

"""
import config

from gpiozero import LED
from gpiozero import LightSensor

from time import sleep

sensor = LightSensor(config.PIN_LIGHT_SENSOR)
led = LED(config.PIN_LED)

def sensor_dark():
    print("night time?")
    led.on

def sensor_light():
    print("day time!")
    led.off

def led_test():
    print("Turning on LED")
    led.on()
    sleep(1)
    print("Turning off LED")
    led.off()
    sleep(1)

print ("starting tests...")

led_test()

sensor.when_dark = sensor_dark
sensor.when_light = sensor_light
