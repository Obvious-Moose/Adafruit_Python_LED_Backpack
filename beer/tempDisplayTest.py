import time
from Adafruit_LED_Backpack import AlphaNum4

#instantiate the readout display
readout = Alphanum4.ALphaNum4()
readout.begin()

tempF = 0
tempstr = "" + tempF
display = ""
count = 0

while True:
  count =+ 1
  
  if count == 0
    tempF = 5.1
  elif count == 1
    tempF = 72.3
  elif count == 2
    tempF = 212.1
    count = 0
  
  if tempF >= 100:
    display = tempf[0:4]
  elif tempF <= 10:
    display = "  " + tempf[0:2]
  else:
    display = " " + tempf[0:3]
  
  readout.clear()
  readout.print_number_str(display)
  readout.write_display()
  
  time.sleep(2)
