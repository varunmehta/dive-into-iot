# Step 4 - Bringing it all together

> Approximate Time: 10-12 minutes

## Checklist

 * IoT thing registered and certificate copied over to pi :heavy_check_mark:
 * Hardware connected :heavy_check_mark:
 * Test program to verify connections run :heavy_check_mark:
 * AWS infrastructure deployed :heavy_check_mark:

Lets go ahead and test it now.

## Run the program

* SSH into the pi
* Run the main python program
```
python3 main.py
```

The program runs an infinite loop, and will only exit when you kill it.
> ^C to kill it

## Switching the LED on/off using API

Get the URL of the API gateway from the notepad.

### Payload to turn on LED

```
{ "led" : "on" }
```

### Payload to turn off LED

```
{ "led" : "off" }
```

### cURL command

```
curl -XPOST \s
     -H "Content-Type: application/json" \
     -d '{ "led" : "off" }' \
     https://<YOUR_URL>.execute-api.us-east-1.amazonaws.com/lab/flasher
```

You can use postman to make these calls too.

## Verify the photocell data in DynamoDB

The second part of the test is to verify if the photocell data is being pushed to DynamoDB.

Here are a couple of tests we can run;

  * Bring out your mobile phones.
  * Turn on the flashlight at 100% and shine on the photocell.
  * Check DynamoDB table data, data should be logged in.
  * Turn off the flashlight & cover the photocell with your hand, or something, that puts the photocell in the dark.
  * Check DynamoDB table data, data should be logged in.

You've now completed the lab successfully.

## What next ?

This is just the start of securly communicating information between the pi & any AWS service. You can connect any sensor or controller to the pi, provide an interface and control it over the internet securely.

 * Capture images via the [pi-camera](https://www.raspberrypi.org/products/camera-module-v2/), send it to rekognition for image processing.
 * Run [Sagemaker-Neo](https://aws.amazon.com/sagemaker/neo/) and run ML models on edge devices.
 * Capture sensor metrics and push to Redshift for analytics.
 * Build POS systems using the pi and interface with bar code scanners and other devices.
 * Add a [touch screen](https://www.raspberrypi.org/products/raspberry-pi-touch-display/) and allow user interaction.
 * [Militarizing Your Backyard with Python: Computer Vision](https://www.youtube.com/watch?v=QPgqfnKG_T4) against Squirrels
