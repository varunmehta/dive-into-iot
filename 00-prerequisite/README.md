# Step 0 - Prerequisite

Before we get started to even work on this tutorial, we need to setup the Pi to even being the process. The folks at [Raspberry Pi Foundation](https://raspberrypi.org) are pretty good with keeping their documentation up to date. The community support surrounding the Pi is also amazing. I'm linking to the respective articles on the foundation website, and that should be good to get you started.

## Buy a Raspberry Pi
 * amazon.com
 * adafruit.com
 * element14.com
 * microcenter.com

For this tutorial a Raspberry Pi 3/4 would be fine. You can also use a Pi-Zero if you are comfortable using the headers and don't need help with WiFi.

## Set up Pi
 * Download [Rasbian](https://www.raspberrypi.org/downloads/raspbian/)
   * For purpose of this tutorial, use the Lite (headless) version, smaller and faster to install.
 * Download [balenaEtcher](https://www.balena.io/etcher/) for your operating system.
 * [Write image to SD card](https://www.raspberrypi.org/documentation/installation/installing-images/).
 * [Enable SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md)
   * Refer point 3 [Enable SSH on a headless Raspberry Pi]
 * [Change `raspi-config` to configure Pi for locale and WiFi](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)
 * Install [gpiozero](https://gpiozero.readthedocs.io/en/stable/installing.html).
   * GPIO Zero is installed by default in the Raspbian image, but keep this handy.
 * [Identify IP Address of the Pi](https://www.raspberrypi.org/documentation/remote-access/ip-address.md)
   * If you don't have access to router, use "Resolving `raspberrypi.local` with mDNS" method.


Once you have setup the Pi, you should be able to SSH into the pi remotely from your local machine. If you are able to do this, move on to step 1.   
