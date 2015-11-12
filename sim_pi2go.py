#!/usr/bin/python3
# pi2go_sim.py
# PiWars 2015 Environment simulation code of the pi2go library
# Author: Nick Young
import cos, sin, radians from math
import threading
import sim_course

# Simulated robot characteristic 
# maximum speed in cm per sec
SIM_SPEED = 6
# width between wheels in cm
SIM_AXLE = 8
# distance from axle to from line sensors in cm
SIM_FRONT = 7
# gap between front line sensors
SIM_GAP =2
# 1 for Full Pi2Go, and 2 for Pi2Go-Lite
SIM_VERSION = 1

# time that robot takes at full speed to do
# a full circle spinning
SIM_TIMESPINCIRCLE = 2
# a full circle turning
SIM_TIMETURNCIRCLE = 3.5

# movement and detection pulse, time in seconds
SIM_PULSE = 0.1

# Position of robot
sim_x = 0
sim y = 0
# Direction of robot in degrees
sim_direction = 90
# Current speed of motors
sim_lspeed = 0
sim_rspeed = 0

sim_initiated = False

sim_thread = Nothing

# General Functions
def init():
	"""Initialises GPIO pins, switches motors and LEDs Off, etc."""
	sim_x = 0
	sim y = 0
	
	sim_direction = 90
	
	sim_lspeed = 0
	sim_rspeed = 0
	
	sim_initiated = True
	
	sim_thread = Timer(SIM_PULSE, sim_move)
	t.start()	 # ten times a second check for movement.

def sim_move():
	if sim_lspeed <> 0 or sim_rspeed <> 0:	# moving
		if sim_lspeed == sim_rspeed:	# straight line
			sim_x += (sim_lspeed / 100.0 * SIM_SPEED * cos(radians(sim_direction)))
			sim_y += (sim_lspeed / 100.0 * SIM_SPEED * sin(radians(sim_direction)))
		else
			if sim_lspeed = -sim_rspeed:	# spinning
				sim_direction += 360 * (SIM_PULSE / SIM_TIMESPINCIRCLE) * (sim_lspeed / 100.0)
			else # turning
				# left wheel arc distance
				#     	wheel speed: circumference of spin divided by time for circle
				#		times duration of movement times percentage of full speed 
				ld = SIM_AXLE*pi() / SIM_TIMESPINCIRCLE * (SIM_PULSE / SIM_TIMESPINCIRCLE) * (sim_lspeed / 100.0)
				#
				rd = SIM_AXLE*pi() / SIM_TIMESPINCIRCLE * (SIM_PULSE / SIM_TIMESPINCIRCLE) * (sim_rspeed / 100.0)
				cur_direction = sim_direction
				sim_direction += 360.0 * (rd-ld) / (SIM_AXLE * 2 * pi())
				sim_lspeed += 0		# placeholder for further calculation
				sim_rspeed += 0		# placeholder for further calculation
	
def cleanup():
	"""Sets all motors and LEDs off and sets GPIO to standard values."""
	sim_lspeed = 0
	sim_rspeed = 0

def version():
	"""Returns 1 for Full Pi2Go, and 2 for Pi2Go-Lite. Invalid until after init() has been called."""
	if sim_initiated:
		return SIM_VERSION


#Motor Functions
def stop():
	"""Stops both motors."""
	sim_lspeed = 0
	sim_rspeed = 0

def forward(speed):
	"""Sets both motors to move forward at speed."""
	if 0 <= speed <= 100:
		sim_lspeed = speed
		sim_rspeed = speed

def reverse(speed):
	"""Sets both motors to reverse at speed."""
	if 0 <= speed <= 100:
		sim_lspeed = -speed
		sim_rspeed = -speed
		

def spinleft(speed):
	"""Sets motors to turn opposite directions at speed."""
	if 0 <= speed <= 100:
		sim_lspeed = -speed
		sim_rspeed = speed

def spinright(speed):
	"""Sets motors to turn opposite directions at speed."""
	if 0 <= speed <= 100:
		sim_lspeed = speed
		sim_rspeed = -speed
	
def turnForward(leftSpeed, rightSpeed):
	"""Moves forwards in an arc by setting different speeds."""
	if (0 <= leftSpeed <= 100) and (0 <= rightSpeed <= 100):
		sim_lspeed = leftSpeed
		sim_rspeed = rightSpeed

def turnreverse(leftSpeed, rightSpeed):
	"""Moves backwards in an arc by setting different speeds."""
	if (0 <= leftSpeed <= 100) and (0 <= rightSpeed <= 100):
		sim_lspeed = -leftSpeed
		sim_rspeed = -rightSpeed	

def go(speed1, speed2=nothing):
	"""controls motors in both directions together with positive/negative speed parameter.
	
	go(leftSpeed, rightSpeed): controls motors in both directions independently using different positive/negative speeds.
	go(speed): controls motors in both directions together with positive/negative speed parameter."""
	if  -100<= speed1 <= 100:
		sim_lspeed = speed1
		sim_rspeed = speed1
		if not speed2 is nothing:
			if -100<=speed2<=100:
				sim_rspeed = speed2




#IR Sensor Functions
def irLeft():
	"""Returns state of Left IR Obstacle sensor."""
	sim_dir_rad = radians(sim_direction)
	irlx = sim_x - SIM_AXLE/2*sin(sim_dir_rad) + SIM_FRONT*cos(sim_dir_rad)
	irly = sim_y + SIM_AXLE/2*cos(sim_dir_rad) + SIM_FRONT*sin(sim_dir_rad)
	return sim_atblock(irlx, irly)

def irRight():
	"""Returns state of Right IR Obstacle sensor."""
	sim_dir_rad = radians(sim_direction)
	irlx = sim_x + SIM_AXLE/2*sin(sim_dir_rad) + SIM_FRONT*cos(sim_dir_rad)
	irly = sim_y - SIM_AXLE/2*cos(sim_dir_rad) + SIM_FRONT*sin(sim_dir_rad)
	return sim_atblock(irrx, irry)

def irAll():
	"""Returns true if any of the Obstacle sensors are triggered."""
	return irLeft or irRight

def irleftLine():
	"""Returns state of Left IR Line sensor."""
	#sim_x, sim_y are centre of robot between axles.
	sim_dir_rad = radians(sim_direction)
	irlx = sim_x-SIM_GAP/2*sin(sim_dir_rad) + SIM_FRONT*cos(sim_dir_rad)
	irly = sim_y+SIM_GAP/2*cos(sim_dir_rad) + SIM_FRONT*sin(sim_dir_rad)
	return sim_online(irlx, irly)

def irRightLine():
	"""Returns state of Right IR Line sensor."""
	#sim_x, sim_y are centre of robot between axles.
	sim_dir_rad = radians(sim_direction)
	irrx = sim_x+SIM_GAP/2*sin(sim_dir_rad) + SIM_FRONT*cos(sim_dir_rad)
	irry = sim_y-SIM_GAP/2*cos(sim_dir_rad) + SIM_FRONT*sin(sim_dir_rad)
	return sim_online(irrx, irry)

# UltraSonic Functions
def getDistance():
	"""Returns the distance in cm to the nearest reflecting object. 0 == no object."""
	return sim_getDistance(sim_x, sim_y, sim_direction)


""" Light Sensor Functions
# (Full Pi2Go only)
#
# getLight(Sensor). Returns the value 0..1023 for the selected sensor, 0 <= Sensor <= 3
# getLightFL(). Returns the value 0..1023 for Front-Left light sensor
# getLightFR(). Returns the value 0..1023 for Front-Right light sensor
# getLightBL(). Returns the value 0..1023 for Back-Left light sensor
# getLightBR(). Returns the value 0..1023 for Back-Right light sensor
"""

# Servo Functions
def startServos():
	"""Initialises the servo background process."""
	pass

def stopServos():
	"""terminates the servo background process."""
	pass

def setServo(Servo, Degrees):
	"""Sets the servo to position in degrees -90 to +90."""
	pass
	

