import time
from Adafruit_LED_Backpack import AlphaNum4
#I guess I got the tempProbe class form Adafruit.  Don't really remember, but I sure didn't write it myself
import tempProbe

#This is for the relay stuff, which probably won't work anyway so who cares.
#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)

#Create an instance of the 14-segment LED Backpack thing, and also the temperature probe dealie
display = AlphaNum4.AlphaNum4()
probe = tempProbe.tempProbe()

#Have to run the display thing once, and also going to clean up the GPIO crap.  Makes sure it's set to off initially.
#I think 22 is the bottom plug and 27 is the top plug.  Only need one for now; no heater.  Ignoring 27 I guess.
display.begin()
#GPIO.cleanup()
#GPIO.setup(22, GPIO.OUT)
#GPIO.setup(27, GPIO.OUT)
#GPIO.output(22, GPIO.LOW)
#GPIO.output(27, GPIO.LOW)

#Variables I might use below
tempF = 0
tempstr = "" + str(tempF)

while True:
  #Get the temperature
  tempF = probe.read_tempF()
  tempstr = "" + str(tempF)
  
  #This parts prints the temp in degrees F on the stupid LED thing.  Wrote this way so it's right-aligned?
  #I doubt this is a good way to do it or whether it even works.  who cares.
  if tempF >= 100:
    display.clear()
    display.print_number_str(tempF[0:4])
  elif tempF <= 10:
    display.clear()
    display.print_number_str("  " + tempf[0:2])
  else:
    display.clear()
    display.print_number_str(" " + tempF[0:3])
  display.write_display()
  
  #This part actually controls the temperature?  It SHOULD flip the relay and turn the cooler on if the beer temp
  #   gets above 74.  Again, I doubt this even works who cares.
  #if tempF > 74:
  #  GPIO.output(22, GPIO.HIGH)
  #elif tempF < 70:
  #  GPIO.output(22, GPIO.LOW)
  
  #Ideally, I'd want to set this to check multiple times.  One reading of 74 could be a fluke (especially given
  #how shitty the probe was when i tested it.)  I'd want it to stay off until it gets 6-10 readings above 74. 
  #Similarly, it shouldn't kick off until it reads below 70 several times.  Doubt what I have works anyway so who cares.
  
  #Pause before the loop.  No need to update everything all that frequently.
  time.sleep(1)
