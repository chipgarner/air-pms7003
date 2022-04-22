# Portable Raspberry Pi air sensor with MQTT conectivity.

The code reads PM values from a PMS7003 sensor via the serial port. Tested on Raspberry Pi, 
but it should work on any machine with Python and serial port. It should also work with the PMS5003 sensor..  It would be
a lot more portable if I had a Pi Zero. 

This program can also display PMS 2.5 on an Adafruit PiOLED - 128x32 Mini OLED (https://www.adafruit.com/product/3527). 
If you are using the display see the instructions below. This display uses I2C and 5 volt power; several similar 
Pi compatible displays should work with minor modifictions.

It can publish MQTT messages and works with ThingsBoard.cloud
Stolen from Device description: <https://aqicn.org/sensor/pms5003-7003/> and other sources with many modifications.

Systemd on Pi (for headless startup of the program on power up) requires installing dependencies using sudo, otherwise they are under user pi and
systemd runs on root and can't find them.


## Setup

To install the driver and MQTT library, simply do:

sudo pip3 install python-aqi

sudo pip3 install paho-mqtt

The Pi file /boot/config.txt needs the line enable_uart=1. this is often the last line.
Check for this with grep uart /boot/config.txt

sudo raspi-config. Shut off access via serial port but leave port enabled.

Raspberry Pi lite OS may need the serial library installed, sudo pip3 pyserial

publisher.py requires an mqtt server and proper credetnials. Just comment out the publisher in pms7003-runner.py 
to run locally on the Pi.

The tests use Pytest. They should run on any machine with the dependencies installed. The tests are not very complete.

To run on startup using systemd copy the contents of the systemd.txt to a .service file in the systemd directory, eg:

sudo nano /etc/systemd/system/yourair.service

Copy the file contents. Edit the ExeStart line, make sure it uses the full path to your python script. Save it and exit, ctrl o to save and ctrl x to exit the nano editor.

Run it:

sudo systemctl start yourair

Check if it's working:

sudo systemctl status yourair

If so enter the following to make it run on start up:

sudo systemctl enable yourair 

If it doesn't work run the following to debug: 

sudo /usr/bin/python3 ~/yourair/pms7003-runner.py


## Usage example

python3 pms7003-runner.py

## Mini Display
For the tiny Adafruit display: https://www.adafruit.com/product/3527

This display uses the 5 Volt pins on the Pi so I wired the power for the pms7003 to one of the USB ports.

The display has several software dependencies. Excellent instructions can be found at 
https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage 
###Here is the abridged version:

sudo pip3 install adafruit-circuitpython-ssd1306

sudo apt-get install python3-pil

Turn on I2C and install Blinka:

sudo pip3 install --upgrade setuptools

cd ~

sudo pip3 install --upgrade adafruit-python-shell

wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py

sudo python3 raspi-blinka.py

Reboot the Pi.

Shut it down again:

sudo shutdown -h now

Plug in the PiOLED and then turn the Pi back on.

python3 pms7003-runner-mini-diplay.py

This should display the latest EPA PMS 2.5 reading in a large font. You can easily cahnge what is displayes, 
see MiniDisplay.py



