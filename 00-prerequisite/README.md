# Step 0 - Prerequisite

> Approximate time: 30-35 minutes

Before we get started with this lab, we need to setup the Raspberry Pi with Rasbian. The folks at [Raspberry Pi Foundation](https://raspberrypi.org) are pretty good with keeping their documentation up to date. The community support surrounding the Pi is also amazing. I've documented the process below, and also linked the respective articles on the foundation's website. It should be good to get you started.

> If you have landed on this repository from an email about the session, then just follow this section, and keep your Pi ready for the hands on lab. If you want to follow ahead on your own, you are more than welcome. Also refer the official documentation, **[Getting Started with AWS IoT](https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html)** for any unanswered questions you might have.

The whole setup should take under 45 minutes, with the longest time spent in downloading the Rasbian image and flashing the SD card.

For this lab a Raspberry Pi 3 B+ or 4 (1 GB or higher) is recommended. You can also use a Pi Zero W, but you'll have to have male headers attached on the GPIO pins.

### Where to buy a Raspberry Pi ?

If this is your first Pi ever, I recommended buying a kit. Even though Pi Zero seems cheaper and will work for this lab, **the regular Pi 4, more powerful and can be repurposed for a lot of different projects**. Here are [some projects](https://projects.raspberrypi.org/en/) you can do with the pi after this lab.

 * https://www.amazon.com
 * https://www.adafruit.com
 * https://www.element14.com
 * https://www.microcenter.com

#### Recommended Kits

> Check with your people manager if they are ready to reimburse the cost of the pi.

Regular Raspberry Pi is just a small single-board computer, it does not come with a power adapater or microSD card. That's where kits come in handy.

 * **[Pi + Power + Case + 32GB microSD card + Micro HDMI to HDMI Cable = $79.99](https://smile.amazon.com/CanaKit-Raspberry-4GB-Starter-Kit/dp/B07V4G63M1/) ~ Recommended**
 * [Pi + Power + Case + Micro HDMI to HDMI Cable = $59.99](https://smile.amazon.com/CanaKit-Raspberry-4GB-Basic-Starter/dp/B07VWBHPMM/) (if you already have a microSD card)

#### À la carte (Build your own kit)
You can also build your own kit using components you might already have. I've tried to list out needed components. All links below are from https://www.microcenter.com. Amazon is more expensive.

| Component | Substitute|Cost|
|-----------|------------|---:|
| [Raspberry Pi 4](https://www.microcenter.com/product/608166/raspberry-pi-4-model-b---1gb-ddr4)  | You can use a Raspberry Pi 3B+ | $35  |
| [Power Suppy](https://www.microcenter.com/product/608169/-raspberry-pi-4-official-15w-power-supply-us---white)  | Fast Charger 15W (5V/3A) <br />  - If you have any mobile phone fast charger and a USB-C cable, check the rating, it it says 5V~3A, it should be good. <br/> - Power hubs are generally restricted to 2.5A, so not a great option.  |$10   |
| [microSD card](https://www.microcenter.com/product/486146/-micro-center-16gb-microsdhc-class-10-flash-memory-card)  |  Any 8GB class 10 microSD card should do, format before using. |$4 |

If you already have a power supply & microSD card, you should be good with only buying a pi.

### Softwares

We are going to transfer files between the Pi and your local machine, and also test the API. Please install the softwares listed below.
 * `ssh` or [putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
 * `scp` or [WinSCP](https://winscp.net/eng/index.php)
 * `curl` or [Postman](https://www.getpostman.com/downloads/)

> `ssh`, `scp` & `curl` are present on Mac and Linux by default. If you have git bash on windows, they might be installed too, please verify.

## Preparing the Pi

We assume by now, you have your trusty raspberry pi with you.

Follow the steps below, links to original source material is also provided where needed. If this documentation feels dated, or inadequate, refer the source links.

### Setup SD Card

Pick a **Class 10 microSD** card with a minimum **8GB** capacity.

Since most IoT devices are remote, using the Lite (headless) version is recommended. It is smaller and uses less resources, without the GUI overhead.

 * Download [Rasbian Buster Lite](https://www.raspberrypi.org/downloads/raspbian/)
 * Download the latest version of [balenaEtcher](https://www.balena.io/etcher/) for your operating system and install it.

#### Flash SD card
 * Connect an SD card reader with the SD card inside.
 * Open balenaEtcher and select from your hard drive the Raspberry Pi `.img` file you wish to write to the SD card.
 * Select the SD card you wish to write your image to.
 * Review your selections and click **'Flash!'** to begin writing data to the SD card.
 * Once complete, etcher might auto eject the card, reinsert the card and move to the next step.

#### Enable SSH

[SSH access is disabled by default](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md)

For headless setup, SSH can be enabled by placing a file named `ssh`, without any extension, onto the `boot` partition of the SD card from another computer. When the Pi boots, it looks for the `ssh` file. If it is found, SSH is enabled and the file is deleted. The content of the file does not matter; it could contain text, or nothing at all.

If you have loaded Raspbian onto a blank SD card, you will have two partitions. The first one, which is the smaller one, is the `boot` partition. Place the file into this one.

This method also works for a GUI based Raspbian.

> **WARNING:** Since you are enabling SSH, please ensure you change the default password, else the pi is vunerable on public networks. More on how to do this below.

#### Setup WiFi on `/boot` before first boot

Setting up [wireless networking](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md) on the pi.

You will need to define a `wpa_supplicant.conf` file for your particular wireless network. Put this file in the `/boot` folder (same location you put the `ssh` file), and when the Pi first boots, it will copy the file to the correct location in the Linux root file system and use those settings to start up wireless networking.

##### `wpa_supplicant.conf` file:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

# Leave this for the lab.
network={
  ssid="J0hnny5"
  psk="Short$ircuit"
  id_str="lab"
}

# Use this for your home network, when preparing the pi
network={
  ssid="<HOME_NETWORK_NAME>"
  psk="<HOME_PASSWORD>"
  id_str="home"
}
```

> Substitute `<HOME_NETWORK_NAME>` & `<HOME_PASSWORD>`, with your current accessible local network SSID and password.

Keep both the networks configurations. They are set in order of preference, if the first is not found, it'll connect to the next available one.

### Boot, Identify Pi on network

Insert the SD card in the pi. Plug in the power cable into your pi, and **wait 1 minute** after boot to start looking for the pi on the network

#### Login to Router and identify

 * In a web browser navigate to your router's IP address e.g. `http://192.168.1.1`,
 * Log in to the router admin panel using your router's credentials.
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

> We'll be changing the `hostname` of your pi later. In a shared network, where all are called `raspberrypi`, you'll not be able to identify your pi.

A detailed write up for [identifing your IP](https://www.raspberrypi.org/documentation/remote-access/ip-address.md) is documented on the offical website.

### Use `raspi-config` to change default configuration

Once you know the IP address, login using `ssh` or `putty`. The default user on Raspbian is `pi` with the password `raspberry`.

```
 ssh pi@192.168.1.131
 password:
```

You'll be shown `raspi-config` on first boot, you can also run it from the command line using

```
sudo raspi-config
```
![raspi-screenshot](https://www.raspberrypi.org/documentation/configuration/images/raspi-config.png)

You should see a blue screen with options in a grey box in the center. [`raspi-config`](https://www.raspberrypi.org/documentation/configuration/raspi-config.md) aims to provide the functionality to make the most common configuration changes.

### Select 4. Localization Options under `raspi-config`

#### Change Locale
Change locale to your local locale `en_US.UTF-8 UTF-8`.

#### Change Time Zone
Select your local time zone, starting with the region, e.g. `Americas`, then selecting a city, e.g. `New_York`. Type a letter to skip down the list to that point in the alphabet.

#### Change keyboard layout

This option opens another menu which allows you to select your keyboard layout. It will take a long time to display while it reads all the keyboard types. Changes usually take effect immediately, but may require a reboot.

Choose `US` keyboard, the default is UK and there are character set differences which can cause issues later.

#### Change WiFi Country

This option sets the country code for your WiFi network. e.g. Change it to `US` (it might already be done as part of `wpa_supplicant` configuration)

> After this step a reboot is recommended, before moving on to the last configuration change. This is due to keyboard layout change. After reboot the IP should still be the same.

### Select 2. Network Options under `raspi-config`

#### Change `hostname`
Set the visible name for this Pi on a network. This is **VERY IMPORTANT**, else you'll not be able to identify your pi in a shared network, especially if all are still called `raspberrypi`. Ensure you make note of the `hostname`, so after reboot you can search for it again, and connect to it.

> Vist [https://videogamena.me/](https://videogamena.me/) for fun server names. Just don't forget what you set it to be!

#### Change Password

The default user on Raspbian is `pi` with the password `raspberry`. You should change that to something more secure.

## Install & Upgrade libraries

### `vim`

`vi` is installed, but `vim` is easier to work with.

```
sudo apt-get install vim
```

For all other editors. Please refer: [this link](https://xkcd.com/378/)

![vim](https://imgs.xkcd.com/comics/real_programmers.png)

Now that you have your pi up and running, it is a good idea to update the system

```
sudo apt-get update
sudo apt-get full-upgrade
```

All the basic tools needed to get you pi for the lab are now set!


## Next --> [01 - Setup IoT Core](../01-iot-core)
This concludes prepping your pi.
