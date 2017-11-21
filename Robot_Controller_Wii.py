#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Robot_Controller_Wii.py
#  
#  Copyright 2017 John Nuber <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from __future__ import print_function
import cwiid, time
import piplates.MOTORplate as MOTOR          #import the MOTORplate module


# ======================================================================
# PyPlate Motor Driver constants and functions
# ======================================================================
# Define Motors
ctl = 1             # controller Address
FL  = 1				# Define Motor 1 = Front Left   - FL
FR  = 2  			# Define Motor 2 = Fright Right - FR
RL  = 3  			# Defome Motor 3 = Rear Left    - RL
RR  = 4  			# Define Motor 4 = Rear Right   - RR

# Define inital motor parameters
speed = 0			# Initalize motor speed 0 - 100
rate  = 30			# Initalize aceleration rate 0 - 100
button_delay = 0.125  # Used by the Wii logic 

# Function to set all drives off
def MotorOff():
    motor.dcSTOP(ctl,FL)
    motor.dcSTOP(ctl,FR)
    motor.dcSTOP(ctl,RL)
    motor.dcSTOP(ctl,RR)
        
    status = "stopped"

def resetCtl():
	MOTOR.clrLED(ctl)
	time.sleep(1)
	MOTOR.RESET(ctl)
	return

def initMotor(FLdir,FRdir,RLdir,RRdir):
	#print("Setting: ",rotation)
	motor.dcCONFIG(ctl,FL,FLdir,0,0)
	motor.dcCONFIG(ctl,FR,FRdir,0,0)
	motor.dcCONFIG(ctl,RL,RLdir,0,0)
	motor.dcCONFIG(ctl,RR,RRdir,0,0)

def fwd():
	# print("Forward motion called. CTL: ",ctl)
	motor.dcCONFIG(ctl,FL,"cw",50,100.0)
	motor.dcCONFIG(ctl,FR,"cw",50,100.0)
	motor.dcCONFIG(ctl,RL,"cw",50,100.0)
	motor.dcCONFIG(ctl,RR,"cw",50,100.0)
	
	motor.dcSTART(ctl,FL)
	motor.dcSTART(ctl,FR)
	motor.dcSTART(ctl,RL)
	motor.dcSTART(ctl,RR)
	
	status = "forward"
	return status

def speed(FLspeed,FRspeed,RLspeed,RRspeed):
	#print("{0}: {1}: {2}: {3}".format(round(LFspeed,2),round(RFspeed,2), round(LRspeed,2),round(RRspeed,2)))
	motor.dcSPEED(ctl,FL,FLspeed)
	motor.dcSPEED(ctl,FR,FRspeed)
	motor.dcSPEED(ctl,RL,RLspeed)
	motor.dcSPEED(ctl,RR,RRspeed)


# ======================================================================
# Initialize PiPlate controller - Address = 1
# ======================================================================
motor = MOTOR
global status

direction = "stopped" # Forward / Backwards / Left / Right
status    = "stopped"

print("Reset and initalize controller {0} and motors".format(ctl))
resetCtl()



# This code attempts to connect to your Wiimote and if it fails the program quits
try:
	for i in range(1,12):
		MOTOR.clrLED(ctl)
		time.sleep(.125)
		MOTOR.setLED(ctl)
		time.sleep(.125)
	print('Please press buttons 1 + 2 on your Wiimote now ...')
	wii=cwiid.Wiimote()
except RuntimeError:
	print("Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!")
	wii = 0
	for i in range(1,8):
		time.sleep(.5)
		MOTOR.setLED(ctl)
		time.sleep(.5)
	wii=cwiid.Wiimote()
	#quit()

print('Wiimote connection established!\n')
wii.rumble = 1
time.sleep(.125)
wii.rumble = 0
time.sleep(.125)
wii.rumble = 1
time.sleep(.125)
wii.rumble = 0
time.sleep(.125)
wii.rumble = 1
time.sleep(.5)
wii.rumble = 0

# print('Go ahead and press some buttons\n')
# print('Press PLUS and MINUS together to disconnect and quit.\n')

time.sleep(1)
wii.rpt_mode = cwiid.RPT_BTN


while True:

  buttons = wii.state['buttons']

  # Detects whether + and - are held down and if they are it quits the program
  #if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
  #  print('\nClosing connection ...')
    # NOTE: This is how you RUMBLE the Wiimote
  #  wii.rumble = 1
  #  time.sleep(1)
  #  wii.rumble = 0
  #  MotorOff()
  #  exit(wii)

  # The following code detects whether any of the Wiimotes buttons have been pressed and then prints a statement to the screen!
  if (buttons & cwiid.BTN_LEFT):
    if status != 'left':
        #print(status)
        MotorOff()  
        initMotor('ccw','cw','ccw','cw')
        status = 'left'
        #print('Motors set to {0}'.format(status))
        rate = 50
        motor.dcSTART(ctl, FL)
        motor.dcSTART(ctl, FR)
        motor.dcSTART(ctl, RL)
        motor.dcSTART(ctl, RR)
        speed(rate,rate,rate,rate)
        #print('...turn left')
    elif status == 'left':
        if rate < 100:
            rate = rate+5
            speed(rate,(rate*.5)+5,rate,rate*.5)
         #   print('Adjusting left turn speed {0}'.format(rate) )
        elif rate == 100 :
            speed(rate,rate,rate,rate)
        #    print('Adjusting left turn speed {0}'.format(rate) )
    time.sleep(button_delay)

  if(buttons & cwiid.BTN_RIGHT):
    if status != 'right':
        #print(status)  
        rate = 50
        MotorOff()
        initMotor('cw','ccw','cw','ccw')
        status = 'right'
        #print('Motors set to {0}'.format(status))
        motor.dcSTART(ctl, FL)
        motor.dcSTART(ctl, FR)
        motor.dcSTART(ctl, RL)
        motor.dcSTART(ctl, RR)
        speed(rate,rate,rate,rate)
        #print('...turn right')
    elif status == 'right':
        if rate < 100:
            rate = rate+5
            speed(rate,(rate*.5)+5,rate,rate*.5)
         #   print('Adjusting right turn speed {0}'.format(rate) )
        elif rate == 100 :
            speed(rate,rate,rate,rate)
         #   print('Adjusting right turn speed {0}'.format(rate) ) 
    time.sleep(button_delay)

  if(buttons & cwiid.BTN_UP):
    if status != 'forward':
        #print(status)  
        #rate = 30
        MotorOff()
        initMotor('ccw','ccw','ccw','ccw')
        status='forward'
        #print('Motors set to {0}'.format(status))
        motor.dcSTART(ctl, FL)
        motor.dcSTART(ctl, FR)
        motor.dcSTART(ctl, RL)
        motor.dcSTART(ctl, RR)
        speed(rate,rate,rate,rate) 
        #print('...forward drive set')
    elif status == 'left':
        motor.dcSTOP(ctl,FR)
        motor.dcSTOP(ctl,RR)
        initMotor('ccw','ccw','ccw','ccw')
        status='forward'
        #print('Motors set to {0}'.format(status))
        motor.dcSTART(ctl, FL)
        motor.dcSTART(ctl, FR)
        motor.dcSTART(ctl, RL)
        motor.dcSTART(ctl, RR)
    elif status == 'right':
        motor.dcSTOP(ctl,FL)
        motor.dcSTOP(ctl,RL)
        initMotor('ccw','ccw','ccw','ccw')
        status='forward'
        #print('Motors set to {0}'.format(status))
        motor.dcSTART(ctl, FL)
        motor.dcSTART(ctl, FR)
        motor.dcSTART(ctl, RL)
        motor.dcSTART(ctl, RR)          
    elif status == 'forward':
        if rate <= 100:
            rate = rate+5
            speed(rate,rate,rate,rate)
           # print('Adjusting speed {0}'.format(rate) )   
    time.sleep(button_delay)

  if(buttons & cwiid.BTN_DOWN):
    rate = rate-5
    if rate >= 30:
        speed(rate,rate,rate,rate)
        #print('Adjusting speed {0}'.format(rate) )     
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_1):
    print('Button 1 pressed')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_2):
    print('Button 2 pressed')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_A):
    if status != 'backwards':
        #print(status)  
        #rate = 30
        MotorOff()
        initMotor('cw','cw','cw','cw')
        status='backwards'
        #print('Motors set to {0}'.format(status))
        motor.dcSTART(ctl, FL)
        motor.dcSTART(ctl, FR)
        motor.dcSTART(ctl, RL)
        motor.dcSTART(ctl, RR)
        speed(rate,rate,rate,rate) 
        #print('...backwards drive set')
    elif status == 'left':
        motor.dcSTOP(ctl,FL)
        motor.dcSTOP(ctl,RL)
        initMotor('ccw','ccw','ccw','ccw')
        status='backwards'
        #print('Motors set to {0}'.format(status))
        motor.dcSTART(ctl, FL)
        motor.dcSTART(ctl, FR)
        motor.dcSTART(ctl, RL)
        motor.dcSTART(ctl, RR)
    elif status == 'right':
        motor.dcSTOP(ctl,FR)
        motor.dcSTOP(ctl,RT)
        initMotor('ccw','ccw','ccw','ccw')
        status='backwards'
       # print('Motors set to {0}'.format(status))
        motor.dcSTART(ctl, FL)
        motor.dcSTART(ctl, FR)
        motor.dcSTART(ctl, RL)
        motor.dcSTART(ctl, RR)          
    elif status == 'backwards':
        if rate <= 100:
            rate = rate+5
            speed(rate,rate,rate,rate)
         #   print('Adjusting speed {0}'.format(rate) )   
    time.sleep(button_delay)
    
  if (buttons & cwiid.BTN_B):
    #print('Motor Stopped')
    MotorOff()
    rate = 30
    status = 'stopped'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_HOME):
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
    check = 0
    while check == 0:
      print(wii.state['acc'])
      time.sleep(0.01)
      check = (buttons & cwiid.BTN_HOME)
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_MINUS):
    print('Minus Button pressed')
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_PLUS):
    print('Plus Button pressed')
    time.sleep(button_delay)

  if (buttons == 0 and status != 'stopped'):
    #MotorOff()
    #status = 'stopped'
    time.sleep(button_delay)
    

  # print('Button: {0}'.format(buttons))
