# PiPiano2

This program was created for use on a Raspberry Pi 3B with the Adafruit MPR121 capacitive touch sensor hat.
This program was created and tested using the Desktop/GUI version of Raspbian Jessie.

### Setup & Installation
Before running this program, you must have installed the following python libraries:  click, pygame, and Adafruit_MPR121.  
Please note that config files use absolute paths to audio files.  The mPiano config files refer to locations in the user's home directory.  These locations will have to be changed to work on your Raspberry Pi.

### Running PiPiano2
The main program file is PiPiano.py
Executable shell files have been created to auto-fill program arguments.

This program is designed to support between 1 and 4 MPR121 hats.  Each hat's address pin must be wired to give it a different I2C address (0x5A, 0x5B, 0x5C, 0x5D).
The flags passed to the python program (-a -b -c -d) tell the program which addresses to use.
The sample and animal instrument sets rely on files that come with a stock raspbian installation.  
Thes files can be found in /usr/share/scracth/Media/Sounds/Animal and /opt/sonic-pi/etc/samples/ .
