# Step 1 - IoT Core

Now that you have your Pi up and running, lets setup the **AWS IoT Core**

## Register Device (Thing)

The steps are short formed from the [**AWS documentation**](https://docs.aws.amazon.com/iot/latest/developerguide/register-device.html)

 * Login to your [AWS Console](https://console.aws.amazon.com)
 * Open [AWS IoT Console](https://console.aws.amazon.com/iot/home)
 * Click **Get Started**
 * On the left navigation pane, choose **Manage**
 * Choose **Register a thing**
   * Any IoT device is called a thing, the thing in our case is the pi.
 * Choose **Create a single thing**
 * Under **Name** enter `PI_<YOURNAME>`.
   * If using a shared account,  this makes it easier to identify it later by your name and delete it.
 * Hit **Next**
 * On the Add a certificate for your thing page, choose Create certificate. This generates an X.509 certificate and key pair.
