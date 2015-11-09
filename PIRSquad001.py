#!/usr/bin/python3
# PiRSquad.py
# simple line follower using pi2go library
# Author: Nick Young

# Import required Python libraries
import time
import pi2go

""" General Functions
init(). Initialises GPIO pins, switches motors and LEDs Off, etc
cleanup(). Sets all motors and LEDs off and sets GPIO to standard values
version(). Returns 1 for Full Pi2Go, and 2 for Pi2Go-Lite. Invalid until after init() has been called
"""

""" Motor Functions
# stop(): Stops both motors
# forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
# reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
# spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
# spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
# turnForward(leftSpeed, rightSpeed): Moves forwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
# turnreverse(leftSpeed, rightSpeed): Moves backwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
# go(leftSpeed, rightSpeed): controls motors in both directions independently using different positive/negative speeds. -100<= leftSpeed,rightSpeed <= 100
# go(speed): controls motors in both directions together with positive/negative speed parameter. -100<= speed <= 100
"""

""" IR Sensor Functions
# irLeft(): Returns state of Left IR Obstacle sensor
# irRight(): Returns state of Right IR Obstacle sensor
# irAll(): Returns true if any of the Obstacle sensors are triggered
# irLeftLine(): Returns state of Left IR Line sensor
# irRightLine(): Returns state of Right IR Line sensor
"""

""" UltraSonic Functions
# getDistance(). Returns the distance in cm to the nearest reflecting object. 0 == no object
"""

""" Light Sensor Functions
# (Full Pi2Go only)
#
# getLight(Sensor). Returns the value 0..1023 for the selected sensor, 0 <= Sensor <= 3
# getLightFL(). Returns the value 0..1023 for Front-Left light sensor
# getLightFR(). Returns the value 0..1023 for Front-Right light sensor
# getLightBL(). Returns the value 0..1023 for Back-Left light sensor
# getLightBR(). Returns the value 0..1023 for Back-Right light sensor
"""

""" Servo Functions
# startServos(). Initialises the servo background process
# stop Servos(). terminates the servo background process
# setServo(Servo, Degrees). Sets the servo to position in degrees -90 to +90
"""

# time that robot takes at full speed to do
# a full circle spinning
timespincircle = 2
# a full circle turning
timeturncircle = 3.5
# ten centimetres
timetencm = 1

# start at half speed
leftspeed = 50
rightSpeed = 50

# go faster or slower depending upon circumstances in the challenge

# Action and start-stop button
action = False

def start_stop(action):
	result = not action
	
	
def wait_for_button_release():
	while getButton[0] = 0:
		sleep(0.1)
	while getButton[0] =1:
		sleep(0.1)

		
# button.when_released = start_stop

def calibrate
	"""Calibrate the robot by spinning left until the left line sensor has changed to dark three times.
	
	Returns nothing"""
	count = 0
	timestart = 0.0
	timeend = 0.0
	online = false
	
	spinLeft(100)
	
	# spin until see dark line
	while irleftLine() = 0
		sleep(0.01)
	online = True
	timestart = time()
	while count < 3
		if irleftLine() > 0:
			if not online:
				online = True
				count += 1
		elif online:
			online = False
		sleep(0.01)
	timeend = time()	
	stop()
	
	
	


def squareup():
	"""Square up to the wall.
	"""
	# square up to the wall
	time5degrees = timespincircle * 5 / 360
	
	# sense distance of wall
	distance_mid = getDistance()
	
	# turn 5 degrees left and sense distance of wall
	spinLeft(50)
	time(timespincircle)
	stop()
	distance_left = getDistance()
	
	# turn back and 5 degrees more right and sense distance of wall
	spinright(50)
	time(0.1+0.1)
	stop()
	distance_right = getDistance()
	
	# turn back to where we started
	spinleft(50)
	time(0.1)
	Stop()
	
	# calculate how much off we are
	rlen = 10	# length of robot for pivot to sensor
	if distance_left > distance_right:
		l[0] = distance_left
		l[1] = distance_mid
	else:
		
	
	# turn to face the wall
	if angle <> 0:
		if angle < 0:
			spinleft(50)	# angle
		else:
			spinright(50)	# angle
		time(t)
		stop()
	
	# return distance to go
	result = getDistance()

def follow_line():
	wait_for_button_release()
	action = start-stop(action)
	
	# start with no turn-rate
	turn = 0.0

	# count steps on this turn-rate
	step = 0
		
	# Start
	while action
		# turn left if left sensor detects dark line
		if irLeftLine() <> 0:
			turn -=
			if turn < 0:
		
			curvecount += 1
			turnForward(min(speed*(1-(curvecount*0.1)),100), min(speed*(1+(curvecount*0.1)),100))
		elif irRightLine() <> 0:
			curvecount += 1
			turnForward(min(speed*(1+(curvecount*0.1)),100), min(speed*(1-(curvecount*0.1)),100))
		else
			curvecount = 0
			# accelerate in straight line
			speed = min(speed+5,100)
			forward(speed)
					
		if getButton[0] = 1:
			# button is pressed to wait for release to flip action state
			while getButton[0] =1:
				time (0.1)
			action = start-stop(action)


"""
Your robot will proceed autonomously from a start line and 
will use sensor(s) to prevent hitting a wooden wall 1.5 metres away. 
It will do this a total of 3 times. 
After each approach and stop, you will retrieve your robot 
and carry it to the start line. 
No part of the robot is permitted to touch the wall, 
so tactile sensors 'feeling' the wall would constitute a failure.
"""		
def proximity_test():
	"""Perform whole PiWars Proximity Test challenge.
	"""
	button.wait_for_press()

	# Start
	while action:
		# drive forward 1.3m so that sensors are in range.
		# use wheel turn calibration on distance
		forward()
		
		# square off to the wall
		distance = squareup(robot)
		
		# proceed towards the wall slowing down as we approach
		# speeed 1 (max) at 20cm and 0 (min) at 0.5cm
		do until distance = 0.5
			robot.forward(distance/19.5)]
			distance = sense_wall()
		
		
def three_point_turn():
	# start inside a marked, A3-sized box.
    
	button.wait_for_press()

	# Start

	while action
		# proceed forward and cross the red line.
		line_sense[0].when_light = robot.stop
		# start measuring outbound distance as count of wheel turns
		forward
		
		# turn left by 90 degrees (either on the spot or in-motion).
		spinleft(50)
		
		
		# drive forward and touch or cross the first black line.
		line_sense[0].when_dark = robot.stop
		robot.forward
		
		# drive backwards in a straight line and touch or cross the first black line.
		line_sense[0].when_dark = robot.stop
		# start measuring across distance as count of wheel turns
		robot.backward()
		
		# drive forwards to the middle of the turning area.
		# move half across distance we have just reversed
		robot.forward()
		
		# turn left by 90 degrees.
		robot.left()
		
		# return to the starting box.
		# move outbound distance back to start
		forward()
		
def straight_line():
	# start inside a marked, A3-sized box.
    
	button.wait_for_press()

	# Start
	
	while action
		

		
# Main loop
challenge = [follow_line(), proximity_test(), three_point_turn()]

# take action depending upon signal
challenge[signal]
