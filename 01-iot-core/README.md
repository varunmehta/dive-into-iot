# Step 1 - IoT Core

> Approximate time: 20-25 minutes

## Before you start
 * Connect your Pi to the network
 * Boot it up
 * Once up and running, identify IP
 * `ssh` into it
 * once connected, proceed to the next step.

> **Please ensure you are able to connect to the pi, moving forward without being able to ssh into the pi, will not let you try out the lab.**

#### Refresher: Boot, Identify Pi on network

Plug in an ethernet cable into your pi, and wait 1 minute after boot to start looking for the pi on the network

A more detailed write up for [identifing your IP](https://www.raspberrypi.org/documentation/remote-access/ip-address.md) is documented on the offical website.

#### Resolving `<YOUR_PI_NAME>.local` with mDNS
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
 mkdir -p /home/pi/iot/certs
 ```
 * Move the downloaded certificates your `private key`, `device certificate`, and a `root certificate authority (CA)` on your local machine to a single empty folder for easier transfer.
 * `scp` or WinSCP the certificate files to `/home/pi/iot/certs`. Run this on local machine, to transfer to pi.
 ```
 cd <certs_folder>

 scp * pi@<YOUR_PI_IP>:~/iot/certs
 ```
 * You now have your certificates on the pi
 * Make symlinks with user friendly names
 ```
  ln -s /home/pi/iot/certs/<YOUR_KEY>private.pem.key /home/pi/iot/certs/private.pem.key
  ln -s /home/pi/iot/certs/<YOUR_KEY>certificate.pem.crt /home/pi/iot/certs/certificate.pem.crt
 ```
 * Download the config.py file from `code/pi/src/config.py` github to your local machine at `/home/pi/iot`
 ```
 wget https://raw.githubusercontent.com/varunmehta/dive-into-iot/master/code/pi/src/config.py
 wget https://raw.githubusercontent.com/varunmehta/dive-into-iot/master/code/pi/src/main.py
  ```

### Modify `config.py`
`config.py` has all the modifiable parameters, which are specific to your setup. We'll change some of the parameters as we've set them up for now.

#### End Point URL

Your Thing has an iot end point, it gets assigned a unique id, which is part of the url.

* Go to list of **Things**
* Click on your **Thing**
* Select **Interact** from the menu on the left.
* Check the `url` under **HTTPS** 

Replace the `<URL>` under `HOST_NAME` to the valid id.
```
# AWS IoT endpoint settings
HOST_NAME = "<URL>-ats.iot.us-east-1.amazonaws.com"
```

#### Verify certificate paths

Just to make things easier, we've already created symlinks to the certs and keys, please ensure the files exist on the path, and the paths specified in the config is valid.
```
# Thing certs & keys
PRIVATE_KEY = "/home/pi/iot/certs/private.pem.key"
DEVICE_CERT = "/home/pi/iot/certs/certificate.pem.crt"
ROOT_CERT = "/home/pi/iot/certs/root-CA.crt"
```

#### MQTT Topics
Replace `<YOUR_THING_NAME>` with the name of the thing you set in the AWS console.
```
# Message settings
PHOTO_RESISTOR_SENSOR = "$aws/things/<YOUR_THING_NAME>/sensor"
FLASHER = "$aws/things/<YOUR_THING_NAME>/flasher"
```

## Next --> [02 - Setup Hardware](../02-hardware)
This concludes our setup of the basic IoT Core on the console and Pi. Let do some hardware wiring...
