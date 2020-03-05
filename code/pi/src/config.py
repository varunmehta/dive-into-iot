"""
# config.py

    Configuration Parameters for your setup.
    Change the values as for your setup.
"""

# AWS IoT endpoint settings
HOST_NAME = "<URL>-ats.iot.us-east-1.amazonaws.com"
HOST_PORT = 8883

# Thing certs & keys
PRIVATE_KEY = "/home/pi/iot/certs/private.pem.key"
DEVICE_CERT = "/home/pi/iot/certs/certificate.pem.crt"
ROOT_CERT = "/home/pi/iot/certs/root-CA.crt"

# Message settings
PHOTO_RESISTOR_SENSOR = "$aws/things/<YOUR_THING_NAME>/sensor"
FLASHER = "$aws/things/<YOUR_THING_NAME>/flasher"
QOS_LEVEL = 1

# GPIO PIN CONFIG
PIN_LIGHT_SENSOR = 18
PIN_LED = 16
