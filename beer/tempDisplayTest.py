import time
from Adafruit_LED_Backpack import AlphaNum4
#I guess I got the tempProbe class form Adafruit.  Don't really remember, but I sure as hell didn't write it myself
import tempProbe

#This is for the relay stuff, which probably won't work anyway so who cares.
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#Create an instance of the 14-segment LED Backpack thing, and also the temperature probe dealie
display = AlphaNum4.AlphaNum4()
probe = tempProbe.tempProbe()

#Have to run the display thing once, and also going to clean up the GPIO crap.  Makes sure it's set to off initially.
#It's a 4-channel relay, but I only need two channels.  Wired to 14, 15, 18, and 23; only going to use 18 and 23.  
#GPIO 18 should be the bottom plug; 23 should be the top.  Went ahead and unplugged 14 and 15 from the relay board.
display.begin()
GPIO.cleanup()
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
GPIO.output(23, GPIO.HIGH)

#Variables I might use below
tempF = 0
tempstr = "" + str(tempF)
lowTrigger = 0
highTrigger = 100
regBool = 0

#Need to ask the user what temps to use
regulation = input("Regulate temperature?  y/n: ")
if regulation == "Y":
  regBool = 1
elif regulation == "y":
  regBool = 1
else:
  regBool = 0
  GPIO.output(18, GPIO.HIGH)
  GPIO.output(23, GPIO.HIGH)

if regBool == 1:
  lowTrigger = input("Select a lower temperature trigger: ")
  highTrigger = input("Select an upper temperature trigger: ")

while True:
  #Get the temperature
  tempF = probe.read_tempF()
  tempstr = "" + str(tempF)
  
  #This parts prints the temp in degrees F on the stupid LED thing.  Wrote this way so it's right-aligned?
  #I doubt this is a good way to do it or whether it even works.  who cares.
  if tempF >= 100:
    display.clear()
    display.print_number_str(tempstr[0:5])
  elif tempF <= 10:
    display.clear()
    display.print_number_str(tempstr[0:3])
  else:
    display.clear()
    display.print_number_str(tempstr[0:4])
  display.write_display()
  
  #This part actually controls the temperature?  It SHOULD flip the relay and turn the cooler on if the beer temp
  #   gets above 74.  Again, I doubt this even works who cares.
  if regBool == 1:
    if tempF > highTrigger:
      GPIO.output(18, GPIO.LOW)
    elif tempF > lowTrigger:
      GPIO.output(18, GPIO.HIGH)
      GPIO.output(23, GPIO.HIGH)
    elif tempF < lowTrigger:
      GPIO.output(23, GPIO.LOW)
  
  #Ideally, I'd want to set this to check multiple times.  One reading of 74 could be a fluke (especially given
  #how shitty the probe was when i tested it.)  I'd want it to stay off until it gets 6-10 readings above 74. 
  #Similarly, it shouldn't kick off until it reads below 70 several times.  Doubt what I have works anyway so who cares.
  
  #Pause before the loop.  No need to update everything all that frequently.
  time.sleep(2)
