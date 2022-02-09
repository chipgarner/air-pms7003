# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT
# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

# Modified Feruary 2022 by Chip Garner

# For Adafruit Adafruit PiOLED - 128x32 Mini OLED

import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


class MiniDisplay:
    def __init__(self):
            
        # Create the I2C interface.
        i2c = busio.I2C(SCL, SDA)
        
        # Create the SSD1306 OLED class.
        # The first two parameters are the pixel width and pixel height.  Change these
        # to the right size for your display!
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
        
        # Clear display.
        self.disp.fill(0)
        self.disp.show()
        
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new("1", (self.width, self.height))
        
        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)
        
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        
        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        self.top = padding
        bottom = self.height - padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0
        
        
        # Load default font.
        self.font = ImageFont.load_default()
        
        # Alternatively load a TTF font.  Make sure the .ttf font file is in the
        # same directory as the python script!
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        # font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)
    
    def loop_me(self):
    
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
    
        # Shell scripts for system monitoring from here:
        # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d' ' -f1"
        IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = 'cut -f 1 -d " " /proc/loadavg'
        CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
        Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    
        # Write four lines of text.
    
        self.draw.text((self.x, self.top + 0), "IP: " + IP, font=self.font, fill=255)
        self.draw.text((self.x, self.top + 8), "CPU load: " + CPU, font=self.font, fill=255)
        self.draw.text((self.x, self.top + 16), MemUsage, font=self.font, fill=255)
        self.draw.text((self.x, self.top + 25), Disk, font=self.font, fill=255)
    
        # Display image.
        self.disp.image(self.image)
        self.disp.show()
        time.sleep(0.1)


if __name__ == '__main__':
    display = MiniDisplay()

    while True:
        display.loop_me()