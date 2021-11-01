#!/usr/bin/python3
# Import libraries
import threading
import time
import math
import sys
import RPi.GPIO as GPIO
import busio
import digitalio
import board
import datetime
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Local Variables
mcp = None       # mcp object
chan_ldr = None  # LDR channel 2 on MCP
chan_mcp = None  # mcp channel 1 on MCP
timer = 1        # Use for finding RunTime
switch = 18      # BCM PIN Number for button, i.e actual is pin 12 on RaspberryPi
counter = 1
start = None


# Setup RPi Pins and peripherals
def setup():
    global mcp, chan_ldr, chan_mcp, switch, length, start
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    GPIO.setmode(GPIO.BCM)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)


    GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

     # create an analog input channel on pin 1 and pin 2
    chan_ldr = AnalogIn(mcp, MCP.P2)
    chan_mcp = AnalogIn(mcp, MCP.P1)

    #Interrupt
    GPIO.add_event_detect(switch, GPIO.FALLING, callback=btn_is_pressed, bouncetime=300)

    
    # Heading
    print("{:<13}{:<20}{:<23}{:}".format("Runtime", "Temp Reading", "Temp","Light Reading"))

    # Start Timer
    start = time.time()

    

# This function repeats
def thread_fuction():
    global mcp, chan_ldr, chan_mcp, timer,start

    x = threading.Timer(timer,thread_fuction)   # Updates interval in thread
    x.daemon = True                             # shutdown when the program exits
    x.start() 

    # Runtime
    Runtime = int(time.time()) - int(start)
    #  start the current thread 
    print("{:}{:<12}{:<20}{:0.3f} {:<16}{:}".format(Runtime,"s",chan_mcp.value, (chan_mcp.voltage - 0.5)*100+1,"C", chan_ldr.value))
           

# Interrupt for the button
def btn_is_pressed(channel):
    global timer, counter
    ls = [1,5,10]

    if counter!=3:
       timer = ls[counter]
       counter+=1

    else:
       counter = 0
       timer = ls[counter]


# resets pins, when the program ends
if __name__ == "__main__":
    try:
       setup()
       thread_fuction()

       while True:
             pass
      
    # Make sure the GPIO is stopped correctly
    except KeyboardInterrupt:
       print("Exiting gracefully")
       GPIO.cleanup()
   
