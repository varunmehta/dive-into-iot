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
    print(" ...ON")
    led.on()
    sleep(1)
    print(" ...OFF")
    led.off()
    sleep(1)

print ("Running LED test...")
led_test()
print ("Bye!")


# while True:
#     sensor.wait_for_active()
#     print("It's light")
#     sensor.wait_for_inactive()
#     print("It's dark")
#
