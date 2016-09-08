#!/usr/bin/env python

###########################################################################
##
## This class controls fans. It can use a config file, or use default
## values. It expects a temperature sensor. It expects two fans, and uses a
## low value and a high value for deciding if it should toggle the fans or
## not. 
##
## This program uses GPIO 11 and 13 for the fans, and 4 for the temp sensor.
##
## Any variable in the variable list can be changed through the config file.
##
## Note: This assumes active low.
##
###########################################################################


class FanController:
    import time #if only it was this easy in real life...
    import RPi.GPIO as GPIO #the class for the pi
    import Adafruit_DHT #the class for the temp sensor
    
    def __init__(self):
        self.GPIO.setmode(self.GPIO.BOARD) #set up the board
        self.sensor = self.Adafruit_DHT.DHT11
        #try to open the config file
        configFile = None
        try:
            configFile = open("config.cfg")
        except:
            print("Error: Config file config.cfg not found.\n")
            exit(1)

        #this is a dictionary of values
        self.variables = {
            "tempSensor":23,
            "fanPinList":[11, 13],
            "lowTemp":75,
            "highTemp":85,
            "checkDelay":60, #seconds
            "reverseLogic":0
        }

        print("opening config file...")
        #go through the config file, reading values
        for line in configFile:
            myLine = line.strip() #strip the whitespace off the line
        
            #make sure there's a line and it's not a comment
            if (len(myLine) > 0 and myLine[0] != "#"):
                #remove the semicolon and everything after it
                myLine = myLine.split(";")[0].strip()
                #split the string over the '='
                pair = myLine.split("=") 
                #print(pair)
                #make sure there are two values (there was an =); otherwise,
                #ignore the line
                if (len(pair) == 2):
                    #set the var name and the value, stripping the semicolon
                    varName, value = pair[0], pair[1]
                    #print(varName, value)
                    #if the variable exists, set it
                    if varName in self.variables:
                        #if the variable is the pin list, parse the list
                        if (varName == "fanPinList"):
                            self.variables[varName] = [int(i) for i in value.strip().split()]
                        #otherwise, just grab the value
                        else:
                            self.variables[varName] = int(value)
        print("closing config file...")
        configFile.close()
        
        try:
            self.GPIO.setup(self.variables["tempSensor"], self.GPIO.IN)
        except:
            print("Error: Could not initialize temperature sensor on pin %d." %self.variables["tempSensor"])
            exit(1)

        self.initFans()

        self.fansOn = False;

        
        #do some output to make sure that the values were picked up
        for i in self.variables:
            print(i, self.variables[i])
    

    #this gets the value of the sensor
    def getTemp(self):
        print("Obtaining temp...")
        humidity, temperature = self.Adafruit_DHT.read_retry(self.sensor, self.variables["tempSensor"])
        print("Finished obtaining temperature.")
        if humidity != None and temperature != None:
            temperature = (temperature * 9.0/5.0) + 32
            print('Temp={0:0.1f}F, Humidity={1:0.1f}%'.format(temperature, humidity))
            return temperature
        else:
            #if the reading failed, return a temperature above the high temperature
            #as a fail safe so that the fans get stuck in the "on" position instead
            #of "off"
            print("Reading failed. Returning temperature above limit.")
            return self.variables["highTemp"] + 1

        #this is useful for testing without an actual temperature monitor.
        # import random as r
        # val = r.randint(self.variables["lowTemp"]-10, self.variables["highTemp"]+10)
        # print("Random temp: %d" %val)
        # return val

    #this returns true or false, based on if the fans are on or off
    def checkFans():
        return self.fansOn
    
    #This turns the fans off.
    def turnFansOn(self):
        if (self.variables["reverseLogic"] == 0):
            for pin in self.variables["fanPinList"]:
                self.GPIO.output(pin, self.GPIO.HIGH)
        else:# self.variables["reverseLogic"] == 1:
            for pin in self.variables["fanPinList"]:
                self.GPIO.output(pin, self.GPIO.LOW)
        self.fansOn = True
        print("Fans turned on.")


    #This turns the fans on.
    def turnFansOff(self):
        if (self.variables["reverseLogic"] == 0):
            for pin in self.variables["fanPinList"]:
                self.GPIO.output(pin, self.GPIO.LOW)
        else:# self.variables["reverseLogic"] == 1:
            for pin in self.variables["fanPinList"]:
                self.GPIO.output(pin, self.GPIO.HIGH)
            self.fansOn = False
        print("Fans turned off.")
        
    def initFans(self):
        print("Initializing fans...")
        pin = 0
        errorCount = 0
        try:
            for pin in self.variables["fanPinList"]:
                self.GPIO.setup(pin, self.GPIO.OUT)
        except:
            print("Error: Fan on pin %d failed to initialize." %pin)
            errorCount += 1
        if (errorCount > 0):
            exit(1)
        self.turnFansOff()

    
    #This starts the monitoring
    def start(self):
        while(1):
            try:
                #This checks to see if the temperature is outside the allowed
                #range. If it is, it toggles the fans accordingly.
                currentTemp = self.getTemp()
                if (currentTemp >= self.variables["highTemp"]):
                    print("Temperature above limit.")
                    if (not self.fansOn):
                        self.turnFansOn()
                elif (currentTemp <= self.variables["lowTemp"]):
                    print("Temperature below limit.")
                    if (self.fansOn):
                        self.turnFansOff()
                else:
                    print("Temperature within range.")

                print("\n")
                self.time.sleep(self.variables["checkDelay"])
            except KeyboardInterrupt:
                print("\n\nProgram Exiting...")
                self.GPIO.cleanup()
                print("Goodbye!\n")
                break

#The main function of this program. Mainly used for testing.
def main():
    f = FanController()

    f.start()



#This starts the program
if __name__ == "__main__":
    main()
