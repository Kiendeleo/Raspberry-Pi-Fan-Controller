#Raspberry Pi Fan Controller

This program uses a temperature sensor to control relays.

To use this program, clone or download the repository, and run install.sh. This will install the library for the temperature monitor from https://github.com/adafruit/Adafruit_Python_DHT , and install this program as an autorun service. Installing will also start the program.

To set up your Raspberry Pi for this program, connect the fans and temperature monitor to GPIO pins and modify the config to tell the program what pins should be used. If you don't do this, then the program can't guess where to send signals and will use the pins predefined in the config.

There are seven values in the config, as follows:
####Settings:
* lowTemp and highTemp: These are temperature values (in degrees F) for the acceptable range. If the temperature is below the lowTemp, the fans will be turned off if they are not already. If above the highTemp, the fans will turn on if they aren't. If the temperature is within the range, no change will be made to the fan state.
* checkDelay: This is the delay, in seconds, between temperature checks. This has been tested to work with a minimum of 1 second.
* reverseLogic: int; 0=False, True otherwise. This is to tell the program if the relays the fans are plugged into are reverse logic or not. By default this is turned on, meaning that the relays are active low (ie, a HIGH signal to the relays turns them off, and a LOW signal to the relays turns them on). If your Pi seems to be doing the opposite of what it should be doing, this is probably set to the wrong setting.
####Pin Configuration
* tempSensor: This is the pin number for the temperature sensor.
* fanPinList: This is a space-separated list of output pins. Any (reasonable) number of pins can be specified. This program has not been tested with an unreasonable number of pins.