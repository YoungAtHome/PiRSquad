#!/usr/bin/python3
# PiRSquad.py
# PiWars 2015 Challenge code using pi2go library
# Author: Nick Young, Jen Young


# Import required Python libraries
import sys

sys.path.append('/home/pi/library/pi2go')
sys.path.append('/home/pi/library/pyusb')
#sys.path.append('/home/pi/library/explorer-hat')

import time
import logging

#import pi2go
import sim_pi2go as pi2go    #simulation library for testing

# Import manual control libraries
import usb.core
import usb.util

# Import control library for skittle 'helmet'
#import explorerhat

USB_IF      = 0 # Interface
USB_TIMEOUT = 5 # Timeout in MS

USB_VENDOR  = 0x1997 # Rii
USB_PRODUCT = 0x0409 # Mini Wireless Keyboard

#USB_VENDOR  = 0x046d # Logitech
#USB_PRODUCT = 0xc52b # K400


# time that robot takes at full speed to do
# a full circle spinning
timespincircle = 2
# a full circle turning
timeturncircle = 3.5
# ten centimetres forwards
time10cm = 1

# start at half speed
leftspeed = 50
rightspeed = 50

# go faster or slower depending upon circumstances in the challenge
#step

dev = None
endpoint = None

# Action and start-stop button
action = False

def start_stop(action):
    return not action

    
#def wait_for_button_release():
#    while pi2go.getButton[0] = 0:
#        sleep(0.1)
#    while pi2go.getButton[0] =1:
#        sleep(0.1)

        
# button.when_released = start_stop

#wait_for_button_release()
#    action = start-stop(action)
    

#code my own sign function rather than import numpy
def my_sign(n): 
    if n < 0:
        return -1
    else:
        return 1    


def calibrate(action):
    """Calibrate the robot by performing the action until the left line sensor has changed 
    to dark three times.
    
    Returns time taken for action"""
    count = 0
    timestart = 0.0
    timeend = 0.0
    online = False
    
    # start the motor action, e.g. spinleft(100)
    action
    
    # act until see dark line
    while pi2go.irLeftLine():
        time.sleep(0.01)
    online = True
    timestart = time.time()
    while count < 2:
        if not pi2go.irLeftLine():
            if not online:
                online = True
                count += 1
        elif online:
            online = False
        time.sleep(0.01)
    timeend = time.time()    
    pi2go.stop()

    logging.debug('Time={}-{}={}'.format(timeend, timestart, (timeend-timestart)/2))
    return (timeend-timestart)/3
    
def calibrate_all():
    global timespincircle
    global timeturncircle
    global time10cm
    logging.info('Calibrating all')

    #timespincircle = calibrate(pi2go.spinLeft(100))
    logging.debug('Time spin'.format(timespincircle))
    #timeturncircle = calibrate(pi2go.turnForward(50,100))
    logging.debug('Time turn'.format(timeturncircle))
    time10cm = calibrate(pi2go.forward(100))
    logging.debug('Time for 10cm='.format(time10cm))


def getmyDistance():
    """Get the distance three times and average

    not time sensitive"""
    d1 = pi2go.getDistance()
    time.sleep(0.05)
    d2 = pi2go.getDistance()
    time.sleep(0.05)
    d3 = pi2go.getDistance()
    time.sleep(0.05)
    # discard outlyers
    if abs(d1 -  (d2 + d3) / 2) < abs(d1) / 10:
        return (d2 + d3) / 2
    elif abs(d2 -  (d1 + d3) / 2) < abs(d2) / 10:
        return (d1 + d3) / 2
    elif abs(d3 -  (d1 + d2) / 2) < abs(d3) / 10:
        return (d1 + d2) / 2
    else:
        return (d1 + d2 + d3) / 3


def square_up():
    speed = 100
    
    """Square up to the wall."""
    # square up to the wall
    time5degrees = timespincircle * 5.0 / 360 * 2
    logging.debug('Time 5 degrees={}'.format(time5degrees))

    # sense distance of wall
    distance_mid = getmyDistance()
    logging.debug('Distance_mid={}'.format(distance_mid))

    # turn 5 degrees left and sense distance of wall
    pi2go.spinLeft(speed)
    time.sleep(time5degrees)
    pi2go.stop()
    distance_left = getmyDistance()
    logging.debug('Distance_left={}'.format(distance_left))

    # turn back and 5 degrees more right and sense distance of wall
    pi2go.spinRight(speed)
    time.sleep(2*time5degrees)
    pi2go.stop()
    distance_right = getmyDistance()
    logging.debug('Distance_right={}'.format(distance_right))

    # turn back to where we started
    pi2go.spinLeft(speed)
    time.sleep(time5degrees)
    pi2go.stop()
    
    # calculate how much off we are
    if distance_left > distance_right:  # scan right for minimum
        distance_old = distance_left
        distance_new = distance_mid
        while distance_new < distance_old:
            logging.debug('Distance old={} new={}'.format(distance_old, distance_new))
            pi2go.spinRight(speed)
            time.sleep(time5degrees / 10.0)
            pi2go.stop()
            distance_old = distance_new
            distance_new = getmyDistance()
        logging.debug('Distance old={} new={}'.format(distance_old, distance_new))
        # spin back
        pi2go.spinLeft(speed)
        time.sleep(time5degrees / 10.0)
        pi2go.stop()
    else:
        # scan left for minimum
        distance_old = distance_right
        distance_new = distance_mid
        while distance_new < distance_old:
            logging.debug('Distance old={} new={}'.format(distance_old, distance_new))
            pi2go.spinLeft(speed)
            time.sleep(time5degrees / 10.0)
            pi2go.stop()
            distance_old = distance_new
            distance_new = getmyDistance()
        logging.debug('Distance old={} new={}'.format(distance_old, distance_new))
        # spin back
        pi2go.spinRight(speed)
        time.sleep(time5degrees / 10.0)
        pi2go.stop()
    exit()
     
    # turn to face the wall
    #if angle <> 0:
    #   if angle < 0:
    #       spinleft(50)    # angle
    #   else:
    #       spinright(50)   # angle
    #   time(t)
    #   stop()
    
    # return distance to go
    distance_mid = getmyDistance()
    logging.debug('Distance_mid={}'.format(distance_mid))
    return distance_mmid

def follow_line():
    """Follow a black line on a white background"""
    #SIM_PULSE = 0.035
    TURN_RATE = 30
    STEP_RATE = 0 #0.5
    SPEED_LINE = 60    
    logging.debug('Turn-rate={} Step-rate={}'.format(TURN_RATE, STEP_RATE))
    # start speed
    speed = SPEED_LINE
    logging.debug('speed={}'.format(speed)) 
    # start with no turn-rate
    turn = 0.0
    # count steps on this turn-rate; use to accelerate
    step = 1
    logging.debug('turn={} step={}'.format(turn, step))
    
    while not pi2go.getSwitch():  #action
        #logging.debug('time0={}'.format(time.time()))
        # turn left if left sensor detects dark line
        if not pi2go.irLeftLine():
            logging.debug('Left')
            if turn > 0:
                step = 0
            #turn = -TURN_RATE
            #turn = max(turn - TURN_RATE, -100)
            speed = TURN_RATE
            turn = -TURN_RATE
        elif not pi2go.irRightLine():
            logging.debug('     Right')
            if turn < 0:
                step = 0
            #turn = TURN_RATE
            #turn = min(turn + TURN_RATE, 100)
            speed = TURN_RATE
            turn = TURN_RATE
        else:
            # no change for now as line is between sensors
            logging.debug('  None  ')
            speed = SPEED_LINE
            turn = 0
            #pass
        
        # accelerate
        step += 1
        #step = min(step + STEP_RATE, 100)
        #logging.debug("turn={} step={}".format(turn, step))
        
        leftspeed = max(min(speed + turn + step * STEP_RATE * my_sign(turn), 100), -100)
        rightspeed = max(min(speed - turn + step * STEP_RATE * my_sign(-turn), 100), -100)
        logging.debug("turn={} step={} lspeed={} rspeed={}".format(turn, step, leftspeed, rightspeed))
        #logging.debug("lspeed={} rspeed={}".format(leftspeed, rightspeed))
        #pi2go.stop()
        #time.sleep(0.5)
        pi2go.go(leftspeed, rightspeed)
        
        # Ignore the time delay to sample as fast as possible.
        #logging.debug('time1={}'.format(time.time()))
        #time.sleep(SIM_PULSE)
        
        # IGNORE button code for now.
        #if getButton[0] = 1:
        #   # button is pressed to wait for release to flip action state
        #   while getButton[0] =1:
        #       time (0.1)
        #   action = start-stop(action)
    pi2go.stop()

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
    MIN_DIST = 1.45

    # drive forward 1.3m so that sensors are in range.
    # use wheel turn calibration on distance
    #pi2go.goBoth(100)
    #time.sleep(time10cm*1)  # test
    #time.sleep(time10cm*13)
    pi2go.stop()
    
    # square off to the wall
    distance = square_up()
    logging.debug('Distance={}'.format(distance))

    # proceed towards the wall slowing down as we approach
    # speeed 1 (max) at 20cm and 0 (min) at 0.5cm
    while distance >= MIN_DIST:
        logging.debug('Speed={}'.format((distance - MIN_DIST) / (20 - MIN_DIST) * 100))
        pi2go.goBoth(min((distance - MIN_DIST) / (20 - MIN_DIST) * 100, 100))
        distance = pi2go.getDistance()
        logging.debug('Distance={}'.format(distance))
    pi2go.stop()
    
def gotoline(speed, over=True):
    """Proceed forward until cross the line."""
    pi2go.goBoth(speed)
    while not pi2go.irLeftLine():
        time.sleep(0.1)
    if over:
        # get off the line
        while pi2go.irLeftLine():
            time.sleep(0.1)

def three_point_turn():
    """Perform three point turn."""
    # start speed
    speed = 100
    # start with no turn-rate
    turn = 100.0
    
    # start inside a marked, A3-sized box.
    
    # proceed forward and cross the red line.
    gotoline(speed, True)
    timestartout = time.time()
            
    # proceed forward and cross the next.
    gotoline(speed, True)
            
    # proceed forward and cross the next.
    gotoline(speed, True)
    timestopout = time.time()
                
    # turn left by 90 degrees (either on the spot or in-motion).
    pi2go.spinLeft(turn)
    time.sleep(timespincircle*90.0/360)
        
    # drive forward and touch or cross the first black line.
    # forward to left line
    timestart = time.time()
    gotoline(speed, False)
    # leave on line
    timestop = time.time()

    # drive backwards in a straight line and touch or cross the first black line.
    # reverse off line and then to right line
    gotoline(-speed, True)
    gotoline(-speed, True)
    
    # drive forwards to the middle of the turning area.
    # move half across distance we have just reversed
    pi2go.goBoth(speed)
    time.sleep(timestop-timestart)

    # turn left by 90 degrees (either on the spot or in-motion).
    pi2go.spinLeft(turn)
    time.sleep(timespincircle*90.0/360)
        
    # return to the starting box.
    # move outbound distance back to start
    pi2go.goBoth(speed)
    time.sleep(timestopout-timestartout)
    
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
    pi2go.goBoth(speed)
    time.sleep(time10cm*2)
    
    pi2go.stop()

    
def controlstart():
    """Manual keyboard control code
    
    Based on example at http://learn.pimoroni.com/tutorial/robots/controlling-your-robot-wireless-keyboard
    
    Use Rii mini-keyboard."""
    global dev, endpoint
    # light.red.on()

    dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)

    logging.info('dev 0:'.format(dev[0]))    
    if len(dev).1: logging.info('dev 0:'.format(dev[1]))    
    endpoint = dev[0][(0, 0)][0]

    if dev.is_kernel_driver_active(USB_IF) is True:
        dev.detach_kernel_driver(USB_IF)
    
    usb.util.claim_interface(dev, USB_IF)
    
    #explorerhat.light.red.off()

def controlend():
    if not dev is None:
        usb.util.release_interface(dev, USB_IF)
        usb.util.dispose_resources(dev)    
    

def manual():
    """Manual control.
    
    Use for straight_line if autonomous mode not working.
    Use for obstacle course if autonomous mode not working.
    Use for joust and skittles."""
    
    BTN_LEFT = 80
    BTN_RIGHT = 79
    BTN_DOWN = 81
    BTN_UP = 82
    BTN_FAST = 28 # Y
    BTN_SLOW = 17 # N
    BTN_STOP = 44 # Space
    BTN_EXIT = 41 # ESC
    
    #explorerhat.light.green.on()
    global leftspeed, rightspeed
    
    while not pi2go.getSwitch():
        control = None
        try:
            control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
            #print(control)
        except:
            pass
        
        if control != None:
            logging.debug('control={}'.format(control))
            if BTN_DOWN in control:
                pi2go.reverse(max(leftspeed, rightspeed))
            
            if BTN_UP in control:
                pi2go.forward(max(leftspeed, rightspeed))
            
            if BTN_LEFT in control:
                pi2go.spinLeft(max(leftspeed, rightspeed))
            
            if BTN_RIGHT in control:
                pi2go.spinRight(max(leftspeed, rightspeed))
            
            if BTN_FAST in control:
                leftspeed = min(leftspeed + 10, 100)
                rightspeed = min(rightspeed + 10, 100)
                logging.debug('leftspeed={} rightspeed={}'.format(leftspeed, rightspeed))
            
            if BTN_SLOW in control:
                leftspeed = max(leftspeed - 10, 0)
                rightspeed = max(rightspeed -10, 0)
                logging.debug('leftspeed={} rightspeed={}'.format(leftspeed, rightspeed))
            
            if BTN_STOP in control:
                pi2go.stop()
            
            if BTN_EXIT in control:
                break
        
        time.sleep(0.02)

    #light.green.off()


def selection():
    """Perform a PiWars challenge, autonomous or manual based on keypress
    
    Current options are:
        follow_line
        proximity_test
        three_point_turn
        manual"""
    global dev, endpoint
      
    BTN_C  = 6
    BTN_F  = 9
    BTN_P = 19
    BTN_S = 22
    BTN_T = 23
    BTN_M = 16
    BTN_Q = 20

    logging.info('Start selection')
    logging.debug('C F P S T M Q')
    while True:
        control = None
        try:
            control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
            logging.debug('Control={}'.format(control))
        except:
            pass

        if control != None:
            if BTN_C in control:
                logging.debug('C for Calibrate')
                calibrate_all()
                
            if BTN_F in control:
                logging.debug('F for Following')
                follow_line()

            if BTN_P in control:
                logging.debug('P for Proximity Test')
                proximity_test()
            
            if BTN_S in control:
                logging.debug('S for Straight Line')
                straight_line()
    
            if BTN_T in control:
                logging.debug('T for Three-point Turn')
                three_point_turn()

            if BTN_M in control:
                logging.debug('M for Manual')
                manual()
                
            if BTN_Q in control:
                logging.debug('Q for Quit')
                break

        time.sleep(0.02)

    #explorerhat.light.green.off()
    
try:
    #logging.basicConfig(filename='robot{}.log'.format(int(time.time())), level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    # Start the robot
    # Initialises GPIO pins, switches motors and LEDs Off, etc
    pi2go.init()
    logging.info('Pi2go initialised')

    controlstart()
    logging.info('USB keyboard initialised')
    
    # Select the action based on keypress
    selection()
    #logging.debug('getDistance()={}'.format(pi2go.getDistance()))
    #while True: #pi2go.getDistance() > 5:
    #    logging.debug('Start')
    #    follow_line()

except:
    controlend()        

finally:
    # Stop motors
    pi2go.stop()

    controlend()
    logging.debug('Release the Keyboard')
    
    # Sets all motors and LEDs off and sets GPIO to standard values
    pi2go.cleanup()
