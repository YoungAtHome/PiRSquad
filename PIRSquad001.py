#!/usr/bin/python3
# PiRSquad.py
# PiWars 2015 Challenge code using pi2go library
# Author: Nick Young, Jen Young

# Import required Python libraries
import time

import pi2go
import pi2go_sim	#simulation library for testing

# Import manual control libraries
import usb.core
import usb.util

# Import control library for skittle 'helmet'
import explorerhat



# time that robot takes at full speed to do
# a full circle spinning
timespincircle = 2
# a full circle turning
timeturncircle = 3.5
# ten centimetres forwards
time10cm = 1

# start at half speed
leftspeed = 50
rightSpeed = 50

# go faster or slower depending upon circumstances in the challenge

# Action and start-stop button
action = False

def start_stop(action):
	result = not action
	
	
#def wait_for_button_release():
#	while getButton[0] = 0:
#		sleep(0.1)
#	while getButton[0] =1:
#		sleep(0.1)

		
# button.when_released = start_stop

#wait_for_button_release()
#	action = start-stop(action)
	
	


def calibrate(action):
	"""Calibrate the robot by performing the action until the left line sensor has changed to dark three times.
	
	Returns time taken for action"""
	count = 0
	timestart = 0.0
	timeend = 0.0
	online = false
	
	# start the motor action, e.g. spinleft(100)
	action
	
	# spin until see dark line
	while not irleftLine():
		sleep(0.01)
	online = True
	timestart = time()
	while count < 3:
		if irleftLine():
			if not online:
				online = True
				count += 1
		elif online:
			online = False
		sleep(0.01)
	timeend = time()	
	stop()
	
	result = (timeend-timestart)/3
	
def calibrate_all():
	global timespincircle
	global timeturncircle
	global time10cm
	
	timespincircle = calibrate(spinLeft(100))
	timeturncircle = calibrate(turnForward(50,100))
	time10cm = calibrate(forward(100))


def square_up():
	"""Square up to the wall."""
	# square up to the wall
	time5degrees = timespincircle * 5.0 / 360
	
	# sense distance of wall
	distance_mid = getDistance()
	
	# turn 5 degrees left and sense distance of wall
	spinLeft(50)
	time(time5degrees)
	stop()
	distance_left = getDistance()
	
	# turn back and 5 degrees more right and sense distance of wall
	spinright(50)
	time(2*time5degrees)
	stop()
	distance_right = getDistance()
	
	# turn back to where we started
	spinLeft(50)
	time(time5degrees)
	Stop()
	
	# calculate how much off we are
	#rlen = 10	# length of robot for pivot to sensor
	if distance_left > distance_right:
        # scan right for minimum
        distance_old = distance_left
        distance_new = diatance_mid
        while distance_new < distance_old:
            spinRight(50)
            time(time5degrees / 10.0)
            Stop()
            distance_old = distance_new
            distance_new = getDistance()
        # spin back
        spinLeft(50)
        time(time5degrees / 10.0)
        Stop()
	else   # scan left for minimum
		distance_old = distance_right
        distance_new = diatance_mid
        while distance_new < distance_old:
            spinLeft(50)
            time(time5degrees / 10.0)
            Stop()
            distance_old = distance_new
            distance_new = getDistance()
        # spin back
        spinRight(50)
        time(time5degrees / 10.0)
        Stop()
	
	# turn to face the wall
	#if angle <> 0:
	#	if angle < 0:
	#		spinleft(50)	# angle
	#	else:
	#		spinright(50)	# angle
	#	time(t)
	#	stop()
	
	# return distance to go
	result = getDistance()

def follow_line():
	"""Follow a black line on a white background"""
    # start speed
    speed = 60
    # start with no turn-rate
	turn = 0.0
	# count steps on this turn-rate; use to accelerate
	step = 0
	
	while True  #action
		# turn left if left sensor detects dark line
		if irLeftLine():
            if turn >= 0:
                step = 0
            turn -= 10
		elif irRightLine():
            if turn <= 0:
                step = 0
            turn += 10
		else
            # no change for now as line is between sensors
            pass
        
        # accelerate
        step += 1
        turnForward(min(speed+turn-step,100), min(speed-turn+step,100))
        
        # IGNORE button code for now.
		#if getButton[0] = 1:
		#	# button is pressed to wait for release to flip action state
		#	while getButton[0] =1:
		#		time (0.1)
		#	action = start-stop(action)


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
	"""Perform whole PiWars Proximity Test challenge."""
	
    # drive forward 1.3m so that sensors are in range.
    # use wheel turn calibration on distance
    go(100)
    time(time10cm*13)
    stop()
    
    # square off to the wall
    distance = square_up(robot)
    
    # proceed towards the wall slowing down as we approach
    # speeed 1 (max) at 20cm and 0 (min) at 0.5cm
    do until distance = 0.5
        go((distance-0.5)/19.5*100)
        distance = getDistance()
    stop()
	
def gotoline(speed, over==True):
    """Proceed forward until cross the line."""
    go(speed)
    while not irLeftLine():
        time(0.1)
    if over:
        # get off the line
        while irLeftLine():
            time(0.1)
		
def three_point_turn():
    """Perform three point turn."""
    # start speed
    speed = 100
    # start with no turn-rate
	turn = 100.0
	
	# start inside a marked, A3-sized box.
    
    # proceed forward and cross the red line.
    gotoline(speed, True)
    timestartout = time()
            
    # proceed forward and cross the next.
    gotoline(speed, True)
            
    # proceed forward and cross the next.
    gotoline(speed, True)
    timestopout = time()
                
    # turn left by 90 degrees (either on the spot or in-motion).
    spinleft(turn)
    sleep(timespincircle*90.0/360)
        
    # drive forward and touch or cross the first black line.
    # forward to left line
    timestart = time()
    gotoline(speed, False)
    # leave on line
    timestop = time()

    # drive backwards in a straight line and touch or cross the first black line.
    # reverse off line and then to right line
    gotoline(-speed, True)
    gotoline(-speed, True)
    
    # drive forwards to the middle of the turning area.
    # move half across distance we have just reversed
    go(speed)
    sleep(timestop-timestart)

    # turn left by 90 degrees (either on the spot or in-motion).
    spinleft(turn)
    sleep(timespincircle*90.0/360)
        
    # return to the starting box.
    # move outbound distance back to start
    go(speed)
    sleep(timestopout-timestartout)
    
    stop()

		
def straight_line():
	"""Straight line speed test."""
    # Full speed
    speed = 100
    
	# start inside a marked, A3-sized box.
    
    # cross the start line
    gotoline(speed, True)
	
    # continue to finish line
    gotoline(speed,True)
    
    # go 20cm further (cross the line)
    go(speed)
    sleep(time10cm*2)
    
	stop()

    
def controlstart():
    """Manual keyboard control code
    
    Based on example at http://learn.pimoroni.com/tutorial/robots/controlling-your-robot-wireless-keyboard
    
    Use Rii mini-keyboard."""
    
    # explorerhat.light.red.on()

    USB_VENDOR  = 0x1997 # Rii
    USB_PRODUCT = 0x2433 # Mini Wireless Keyboard

    USB_IF      = 0 # Interface
    USB_TIMEOUT = 5 # Timeout in MS

    dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)
    endpoint = dev[0][(0,0)][0]

    if dev.is_kernel_driver_active(USB_IF) is True:
        dev.detach_kernel_driver(USB_IF)

    usb.util.claim_interface(dev, USB_IF)
    
    #explorerhat.light.red.off()

def controlend():
    usb.util.
    pass
    

def manual():
    """Manual control.
    
    Use for straight_line if autonomous mode not working.
    Use for obstacle course if autonomous mode not working.
    Use for joust and skittles."""

    BTN_LEFT  = 80
    BTN_RIGHT = 79
    BTN_DOWN  = 81
    BTN_UP    = 82
    BTN_STOP  = 44 # Space
    BTN_EXIT  = 41 # ESC

    #explorerhat.light.green.on()

    while True:
        control = None
        try:
            control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
            #print(control)
        except:
            pass

        if control != None:
            if BTN_DOWN in control:
                reverse(max(leftSpeed, rightSpeed))

            if BTN_UP in control:
                forward(max(leftSpeed, rightSpeed))
                
            if BTN_LEFT in control:
                spinLeft(max(leftSpeed, rightSpeed))

            if BTN_RIGHT in control:
                spinRight(max(leftSpeed, rightSpeed))
                
            if BTN_STOP in control:
                stop()

            if BTN_EXIT in control:
                break

        time.sleep(0.02)

    #explorerhat.light.green.off()

def selection():
    """Perform a PiWars challenge, autonomous or manual based on keypress
    
    Current options are:
        follow_line
        proximity_test
        three_point_turn
        manual"""
      
    BTN_C  = 6
    BTN_F  = 9
    BTN_P = 19
    BTN_T = 23
    BTN_M = 16
    BTN_Q = 20
    
    while True:
        control = None
        try:
            control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
            #print(control)
        except:
            pass

        if control != None:
            if BTN_C in control:
                calibrate_all()
                
            if BTN_F in control:
                follow_line()

            if BTN_P in control:
                proximity_test()
                
            if BTN_T in control:
                three_point_turn()

            if BTN_M in control:
                manual()
                
            if BTN_Q in control:
                break

        time.sleep(0.02)

    #explorerhat.light.green.off()
    
try:
    # Start the robot
    # Initialises GPIO pins, switches motors and LEDs Off, etc
    init()
    
    # Select the action based on keypress
    selection()
    
finally:
    # Stop motors
    stop()
    
    # Sets all motors and LEDs off and sets GPIO to standard values
    cleanup()
