# A minimalistic python interface for PMS7003 sensor

The code reads PM values from serial port. Tested on Raspberry Pi, 
but it should work on any machine with Python and serial port.

Stolen from Device description: <https://aqicn.org/sensor/pms5003-7003/> with many modifications.


Systemd on Pi requires installing dependencies using sudo, otherwise they are under user pi and
systemd runs on root and can't find them.


## Setup

To install the driver, simply do:

sudo pip3 install python-aqi
sudo pip3 install paho-mqtt

The Pi file /boot/config.txt needs the line enable_uart=1. this is often the last line.
Check for this with grep uart /boot/config.txt

sudo raspi-config. shut off access via serial port

publisher.py requires an mqtt server and proper credetnials. Just comment out the publisher in pms7003-runner.py 
to run locally on the Pi.

To run on startup using systemd copy the contents of the systemd.txt to a .service file in the systemd directory, eg:
sudo nano /etc/systemd/system/pms7003.service
copy the file contents, save it and exit, ctrl o to save and ctrl x to exit the nano editor.

Run it:
sudo systemctl start pms7003
Check if it's working:
systemctl status pms7003
If so enter the following to make it run on start up:
sudo systemctl enable pms7003 

If it doesn't work run sudo /usr/bin/python3 /home/pi/Sensors/air-pms7003/pms7003-runner.py to debug.
## Usage example

python3 pms7003-runner.py
