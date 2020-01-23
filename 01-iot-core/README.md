# Step 1 - IoT Core

> Approximate time: 20-25 minutes

## Before you start
 * Connect your Pi to the network
 * Boot it up
 * Once up and running, identify IP
 * `ssh` into it
 * once connected, proceed to the next step.

> **Please ensure you are able to connect to the pi, moving forward without being able to ssh into the pi, is be a blocker for this lab.**

##### Refresher: Boot, Identify Pi on network

Plug in an ethernet cable into your pi, and wait 1 minute after boot to start looking for the pi on the network

A more detailed write up for [identifing your IP](https://www.raspberrypi.org/documentation/remote-access/ip-address.md) is documented on the offical website.

##### Resolving `<YOUR_PI_NAME>.local` with mDNS
 * Open terminal
 * Type `ping <YOUR_PI_NAME>.local`
 * If the Raspberry Pi is reachable, `ping` will show its IP address
```
  PING <YOUR_PI_NAME>.local (192.168.1.131): 56 data bytes
  64 bytes from 192.168.1.131: icmp_seq=0 ttl=255 time=2.618 ms
```
----

## 1a. AWS IoT Console

### What are we doing here ?
 * Register our device (thing) with AWS console.
 * Create IoT policy
 * Attach certificate to IoT policy
 * Attach certificate to thing

Now that you have your Pi up and running, lets setup the **IoT Core** on the AWS console. Where ever the document says `<YOURNAME>`, replace it with your name or a user friendly name, which can help you identify your device and policies later.

> *If the commit date on this is older than 6 months, please also refer the [offical documentation](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html) for any new updates.*

The steps are borrowed & short formed from the orignal [**AWS documentation**](https://docs.aws.amazon.com/iot/latest/developerguide/register-device.html)

### Create Policy
 * On your current machine, browse to the [**AWS IoT console**](https://console.aws.amazon.com/iot/home).
 * In the navigation pane, choose **Secure**, and then choose **Policies**.
 * On the **Policies** page, choose **Create a policy**.
 * On the **Create a policy** page:
 * Enter a **name** for the policy (for example, `<YOURNAME>-Policy`).
 * For **Action**, enter `iot:*`
 * For **Resource ARN**, enter `*`
 * Under **Effect**, choose **Allow**, and then choose **Create**.
 * This policy allows your Raspberry Pi to publish messages to AWS IoT.

> **Important** These settings are overly permissive. In a production environment narrow the scope of the permissions to that which are required by your device.

### Register Device (Thing)
 * In the console navigation pane, choose **Manage**, and then choose **Things**.
 * Choose **Create**.
 * On the **Creating AWS IoT things** page, choose **Create a single thing**.
 * On the **Add your device** to the device registry page, enter **`<YOURNAME>`_PI**, and then choose **Next**.

### Generate & Attach Certificates
Certificates are what ensures a secure communication between your Pi and the cloud services. In this step, we generate certificates and install them on the pi.

 * On the **Add a certificate** for your thing page, choose **Create certificate**.
 * On the **Certificate created** page, download your `private key`, `device certificate`, and a `root certificate authority (CA)` for AWS IoT. (Choose the Download link for each)
  > These files are saved in your downloads directory.
 * Choose **Activate** to activate the X.509 certificate, and then choose **Attach a policy**.
 * On the **Add a policy** for your thing page, choose `<YOURNAME>-Policy` and then choose **Register Thing**.

----

## 1b. The Pi

> **IMPORTANT: Please ensure you are able to connect to the pi, moving forward without being able to ssh into the pi, is be a blocker for this lab.**




> For the following steps, you can either `ssh` into the pi and make changes there, or make changes on your local and `scp` the files to the pi
>
> Feel free to substitute `vim` with your [favourite text editor](https://xkcd.com/1823/)

### Certificate installation

 * Open terminal
 * `ssh` into the pi
    ```
    ssh pi@<IP_ADDRESS>
    password: <SUPER_SECRET_PASSWORD>
    ```
 * Create a working directory under `/home/pi`, this is where we'll copy our certificates and python code.
 ```
 mkdir -p iot/certs
 ```
 * 
