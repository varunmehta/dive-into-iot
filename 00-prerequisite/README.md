# Step 0 - Prerequisite

Before we get started to even work on this tutorial, we need to setup the Pi to even being the process. The folks at [Raspberry Pi Foundation](https://raspberrypi.org) are pretty good with keeping their documentation up to date. The community support surrounding the Pi is also amazing. I'm picking the needed points, and linking to the respective detailed articles on the foundation's website. It should be good to get you started.

> If you have landed on this repository from an email about the hands-on session, then just do this section, and keep your Pi ready for the lab. If you want to finish the whole lab on your own, you are more than welcome. Also refer **"[Getting Started with AWS IoT](https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html)"** guide.

The whole setup should take under an hour, the longest time spent in downloading the image and flashing the SD card.

For this lab a Raspberry Pi 3/4 will be fine. You can also use a Pi-Zero if you are comfortable using the headers and don't need help with WiFi.

### Where to buy a Raspberry Pi ?
 * amazon.com
 * adafruit.com
 * element14.com
 * microcenter.com

## Preparing the Pi

We assume you have your trusty raspberry pi with you.

Follow the steps below, links to original source material is also provided, if this documentation feels out of date, or inadequate, refer the source links.

### Setup SD Card

Pick a **Class 10 microSD** card with a minimum **8GB** capacity.

Since most IoT devices are remote, using the Lite (headless) version is better. It is smaller and faster to install, without the GUI overhead

 * Download [Rasbian Buster Lite](https://www.raspberrypi.org/downloads/raspbian/)
 * Download the latest version of [balenaEtcher](https://www.balena.io/etcher/) for your operating system and install it.

#### Flash SD card
 * Connect an SD card reader with the SD card inside.
 * Open balenaEtcher and select from your hard drive the Raspberry Pi .img file you wish to write to the SD card.
 * Select the SD card you wish to write your image to.
 * Review your selections and click **'Flash!'** to begin writing data to the SD card.
 * Once complete, etcher might auto eject the card, reinsert the card and move to the next step.

#### Enable SSH

The latest versions of Rasbian, disable SSH access by default.

For headless setup, SSH can be enabled by placing a file named ssh, without any extension, onto the boot partition of the SD card from another computer. When the Pi boots, it looks for the ssh file. If it is found, SSH is enabled and the file is deleted. The content of the file does not matter; it could contain text, or nothing at all.

If you have loaded Raspbian onto a blank SD card, you will have two partitions. The first one, which is the smaller one, is the boot partition. Place the file into this one.

This method also works for a [GUI based](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md) Raspbian too.

> **WARNING:** Since you are enabling SSH, please ensure you change the default password, else the pi is vunerable on public networks. More on this below


#### Setup WiFi on `/boot` before first boot

If you don't have the wired setup easily accessible, you can also setup [wireless networking](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md) on the pi.

You will need to define a `wpa_supplicant.conf` file for your particular wireless network. Put this file in the /boot folder (same place you put the `ssh` file), and when the Pi first boots, it will copy that file into the correct location in the Linux root file system and use those settings to start up wireless networking.

`wpa_supplicant.conf` file example:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
 ssid="<Name of your WiFi>"
 psk="<Password for your WiFi>"
}
```

### Boot, Identify Pi on network

Plug in an ethernet cable into your pi, and wait 1 minute after boot to start looking for the pi on the network

A more detailed write up for [identifing your IP](https://www.raspberrypi.org/documentation/remote-access/ip-address.md) is documented on the offical website.

#### Login to Router and identify

 * In a web browser navigate to your router's IP address e.g. `http://192.168.1.1`,
 * Log in to the router admin panel using your credentials.
 * Browse to the list of connected devices or similar (all routers are different), and you should see some devices you recognise.
 * Figure out which is your Raspberry Pi. Also note the connection type; if your Pi is connected with a wire there should be fewer devices to choose from.

#### Resolving `raspberrypi.local` with mDNS

 * Open terminal
 * Type `ping raspberrypi.local`
 * If the Raspberry Pi is reachable, `ping` will show its IP address
```
   PING raspberrypi.local (192.168.1.131): 56 data bytes
   64 bytes from 192.168.1.131: icmp_seq=0 ttl=255 time=2.618 ms
```

### Use `raspi-config` to change default configuration

Once you know the IP address of your pi, login using `ssh` or `putty`. The default user on Raspbian is `pi` with the password `raspberry`.

```
 ssh pi@192.168.1.131
 password:
```

You'll be shown `raspi-config` on first boot, you can also run it from the command line using

```
sudo raspi-config
```

You should see a blue screen with options in a grey box in the centre. [`raspi-config`](https://www.raspberrypi.org/documentation/configuration/raspi-config.md) aims to provide the functionality to make the most common configuration changes.


#### Change locale
Change locale to your local locale `en_US.UTF-8 UTF-8`.

#### Change time zone
Select your local time zone, starting with the region, e.g. Americas, then selecting a city, e.g. New_York. Type a letter to skip down the list to that point in the alphabet.

#### Change WiFi Country

This option sets the country code for your WiFi network. e.g. Change it to `US`

#### Change keyboard layout
This option opens another menu which allows you to select your keyboard layout. It will take a long time to display while it reads all the keyboard types. Changes usually take effect immediately, but may require a reboot.

> After this step a reboot is recommended, before moving on to the last configuration change. This is due to keyboard layout change.

#### Change Password

The default user on Raspbian is `pi` with the password `raspberry`. You should change that to something more secure.

## Update all libraries

Now that you have your pi up and running, it is a good idea to update the system

```
sudo apt-get update
sudo apt-get full-upgrade
```

All the basic tools needed to get you pi for the lab are now set!
