"""
# main.py
    This is the main program.
     * Flash LEDs on MQTT commands
     * Log status of light sensor
"""
import json
import config
import logging

from gpiozero import LED
from gpiozero import LightSensor
from time import sleep
from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# LightSensor is connected to this pin.
sensor = LightSensor(config.PIN_LIGHT_SENSOR)
led = LED(config.PIN_LED)


def lps(message):
    """
        L: Log
        P: Print to console
        S: Send to AWS
        This method is supposed to log the message to log4j, print to console (for testing),
        and send the message to be logged as an event. All events are logged.
    """
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")

    print('[ ' + now + ' ] ' + message)
    message = '{ "state": "' + message + '", "timestamp": "' + now + '"}'
    message = json.dumps(message)
    message = json.loads(message)
    try:
        client.publishAsync(config.SENSOR, message, 0)
    except AWSIoTMQTTClient.exception.AWSIoTExceptions.publishTimeoutException as e:
        print(e)


def blink_led(led_cmd):
    """
        Logic to turn led on-off.
    """
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")

    print('[ ' + now + ' ] ' + led_cmd )

    if led_cmd == "blink":
        led.on()
        sleep(1)
        print(" ...OFF")
        led.off()
        lps("blinked")
    else:
        print("garbage command")
        lps("garbage command received")


def handle_subscription(client, userdata, message):
    """
        Call back method called for every subscription
        Where message contains topic and payload.
        Note: client and userdata are pending to be deprecated and should not be depended on.
    """
    payload = message.payload
    payload = payload.decode('utf-8')
    print(payload)
    # for now printing message, figure out more on payload and play with it.
    lps("Request received on topic: " + str(message.topic) + ", with payload: " + payload)
    blink_led(payload)


# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Initialize MQTT client
client = AWSIoTMQTTClient('')

# Configure client endpoint, port information, certs
client.configureEndpoint(config.HOST_NAME, config.HOST_PORT)
client.configureCredentials(config.ROOT_CERT, config.PRIVATE_KEY, config.DEVICE_CERT)
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)
client.subscribe(config.FLASHER, 1, handle_subscription)

# Connect
print('Connecting to endpoint ' + config.HOST_NAME)

client.connect()

while True:
    """
        To infinity and beyond!
    """
