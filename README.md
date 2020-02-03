# Dive into IoT using AWS & Raspberry Pi

> Approximate time: 90 minutes


Welcome to **Dive into IoT**. This is a simple hands on lab to get you started with AWS IoT using the Raspberry Pi.

> If you have landed on this repository from an email about the hands on session, then just follow [**00 - Prerequisite**](00-prerequisite), and keep your Pi ready for the hands on lab. If you want to follow ahead on your own, you are more than welcome. Also refer the official documentation, **[Getting Started with AWS IoT](https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html)** for any unanswered questions you might have.

## Architecture Overview
![Architecture Overview](assets/dive-into-iot.png)

## What do you need ?
 * [**Raspberry Pi**](https://raspberrypi.org), with power supply & Class 10 microSD card, [loaded with Rasbian, libraries and wifi setup](/00-prerequisite).
 * A valid AWS account with rights to create IAM roles, and accesss needed AWS services
   * IAM roles
   * DynamoDB
   * Lambda functions
   * IoT core
   * API Gateway

> You can always [sign up for a free tier account](https://portal.aws.amazon.com/billing/signup#/start) for this lab

### Additional Hardware ~ provided during the lab

  * [Photo cell](https://www.adafruit.com/product/161)
  * [LEDs](https://www.adafruit.com/product/4202)
  * Resistors of LEDs
  * Female-to-Female jumper cables (to connect components to header).

### Softwares

We are going to transfer files between the Pi and your local machine, and also test the API. Please install the softwares listed below.
 * `ssh` or [putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
 * `scp` or [WinSCP](https://winscp.net/eng/index.php)
 * `curl` or [Postman](https://www.getpostman.com/downloads/)

## What will we do ?
 * Connect sensors (input) to GPIO ports
 * Collect sensor state and push to DynamoDB
 * Connect LEDs (output) on the Raspberry Pi
 * Post requests to API Gateway, and control state of LED (turn it on-off)

## How will we do ?
 * **[00 - Prerequisite](/00-prerequisite)** ~ Follow this to ready your pi for the hands on lab.
 * **[01 - Setup IoT Core](/01-iot-core)**
 * **[02 - Setup Hardware](/02-hardware)**
 * **[03 - Build AWS supporting infrastructure](/03-infrastructure)**
 * **[04 - End-to-end connections](/04-end-to-end)**

## Learning

By the end of this session, you should have a basic idea on how to setup a raspberry pi with AWS IoT and send/receive data from pi to cloud securely over the internet.

There is a lot more information available, about fleet management, RTOS, Greengrass. **[Check the AWS documentation](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html)** for more details.

## Start --> [00 - Prerequisite](/00-prerequisite)
Lets prep to pi for the lab...
