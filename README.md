#Raspberry Pi Fan Controller

This program uses a temperature sensor to control two fans.

parse.py is the controller for the pi. It sets up the GPIO and starts checking the temperature and toggling the fans every so often. The pin numbers for the two fans and the temperature reader, the high and low temperatures for toggling, the delay between temperature checks, and an option for reverse logic can all be modified in the config.