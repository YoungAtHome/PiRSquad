#!/usr/bin/python3
#pi2go_sim.py
"""PiWars 2015 Environment simulation code of the pi2go library
    Author: Nick Young"""
from math import cos, sin, radians
import threading
import sim_course
import logging
import time

# Simulated robot characteristic
# Two wheel robot
# maximum speed in cm per sec
SIM_SPEED = 6
# width between wheels in cm
SIM_AXLE = 8
# distance from axle to from line sensors in cm
SIM_FRONT = 7
# gap between front line sensors
SIM_GAP = 2
# 1 for Full Pi2Go, and 2 for Pi2Go-Lite
SIM_VERSION = 1

# movement and detection pulse, time in seconds
SIM_PULSE = 0.1

# Position of robot
# mid-point between wheels
sim_x = 10
sim_y = 30
# Direction of robot in radians
sim_direction = radians(90)
# Current speed of motors, 0 <= speed <= 100
sim_lspeed = 0
sim_rspeed = 0

sim_initiated = False

sim_thread = None

# General Functions
def init():
    """Initialises GPIO pins, switches motors and LEDs Off, etc."""

    #log constants
    #logging.basicConfig(filename = 'sim.log', level=logging.DEBUG)

    logging.info('SIM:Speed={}'.format(SIM_SPEED))
    logging.info('SIM:Pulse={}'.format(SIM_PULSE))

    global sim_x, sim_y, sim_direction, sim_lspeed, sim_rspeed, sim_initiated, sim_thread
    sim_x = 0
    sim_y = 0
    logging.info('SIM:x={} y={}'.format(sim_x, sim_y))
    
    sim_direction = radians(90)
    logging.info('SIM:Directiom={}'.format(sim_direction))

    sim_lspeed = 0
    sim_rspeed = 0
    logging.info('SIM:lspeed={} rspeed={}'.format(sim_lspeed, sim_rspeed))

    sim_initiated = True

    sim_thread = threading.Timer(SIM_PULSE, sim_move)
    sim_thread.start()    # ten times a second check for movement.

def sim_move():
    """Move robot distance and direction for one pulse."""
    global sim_x, sim_y, sim_direction
    logging.debug('SIM:time={}'.format(time.time()))
    if sim_lspeed != 0 or sim_rspeed != 0:    # moving
        logging.info('SIM:move() lspeed={} rspeed={}'.format(sim_lspeed, sim_rspeed))
        if sim_lspeed == sim_rspeed:    # straight line
            sim_x += (sim_lspeed / 100.0 * SIM_SPEED / SIM_PULSE * cos(sim_direction))
            sim_y += (sim_lspeed / 100.0 * SIM_SPEED / SIM_PULSE * sin(sim_direction))
            logging.info('SIM:x={} y={}'.format(sim_x, sim_y))
        else:
            # right wheel arc distance is percentage of full speed in time of pulse
            rd = SIM_SPEED * (sim_rspeed / 100.0) * SIM_PULSE
            if sim_lspeed == -sim_rspeed:    # spinning
                # angle in radians is arc length over radius
                sim_direction += rd / (SIM_AXLE / 2.0) 
                logging.info('SIM:Directiom={}'.format(sim_direction))
            else: # turning
                # left wheel arc distance
                #         wheel speed: circumference of spin divided by time for circle
                #        times duration of movement times percentage of full speed 
                ld = (sim_lspeed / 100.0) * SIM_SPEED * SIM_PULSE
                rd = (sim_rspeed / 100.0) * SIM_SPEED * SIM_PULSE
                cur_direction = sim_direction
                
                # inner radius
                r = (SIM_AXLE * rd) / (ld + rd)
                sim_direction += (r * ld)
                logging.info('SIM:Directiom={}'.format(sim_direction))

                # chord length is 2R sin (theta / 2)
                d = 2 * (r + SIM_AXLE / 2) * sin(cur_direction / 2)
                
                sim_x += d * cos(sim_direction)
                sim_y += d * sin(sim_direction)
                logging.info('SIM:x={} y={}'.format(sim_x, sim_y))


def cleanup():
    """Sets all motors and LEDs off and sets GPIO to standard values."""
    global sim_lspeed, sim_rspeed
    sim_lspeed = 0
    sim_rspeed = 0
    
    if not sim_thread is None:
        sim_thread.cancel()

def version():
    """Returns 1 for Full Pi2Go, and 2 for Pi2Go-Lite. Invalid until after init() has been called."""
    if sim_initiated:
        return SIM_VERSION


#Motor Functions
def stop():
    """Stops both motors."""
    global sim_lspeed, sim_rspeed
    sim_lspeed = 0
    sim_rspeed = 0

def forward(speed):
    """Sets both motors to move forward at speed."""
    global sim_lspeed, sim_rspeed
    if 0 <= speed <= 100:
        sim_lspeed = speed
        sim_rspeed = speed
        logging.info('SIM:forward() lspeed={} rspeed={}'.format(sim_lspeed, sim_rspeed))

def reverse(speed):
    """Sets both motors to reverse at speed."""
    global sim_lspeed, sim_rspeed
    if 0 <= speed <= 100:
        sim_lspeed = -speed
        sim_rspeed = -speed
        

def spinLeft(speed):
    """Sets motors to turn opposite directions at speed."""
    global sim_lspeed, sim_rspeed
    if 0 <= speed <= 100:
        sim_lspeed = -speed
        sim_rspeed = speed

def spinRight(speed):
    """Sets motors to turn opposite directions at speed."""
    global sim_lspeed, sim_rspeed
    if 0 <= speed <= 100:
        sim_lspeed = speed
        sim_rspeed = -speed
    
def turnForward(leftSpeed, rightSpeed):
    """Moves forwards in an arc by setting different speeds."""
    global sim_lspeed, sim_rspeed
    if (0 <= leftSpeed <= 100) and (0 <= rightSpeed <= 100):
        sim_lspeed = leftSpeed
        sim_rspeed = rightSpeed
        logging.info('SIM:turnforward() lspeed={} rspeed={}'.format(sim_lspeed, sim_rspeed))

def turnReverse(leftSpeed, rightSpeed):
    """Moves backwards in an arc by setting different speeds."""
    global sim_lspeed, sim_rspeed
    if (0 <= leftSpeed <= 100) and (0 <= rightSpeed <= 100):
        sim_lspeed = -leftSpeed
        sim_rspeed = -rightSpeed    

def go(speed1, speed2 = None):
    """controls motors in both directions together with positive/negative speed parameter.
    
    go(leftSpeed, rightSpeed): controls motors in both directions independently using different positive/negative speeds.
    go(speed): controls motors in both directions together with positive/negative speed parameter."""
    global sim_lspeed, sim_rspeed
    if  -100 <= speed1 <= 100:
        sim_lspeed = speed1
        sim_rspeed = speed1
        if speed2 != None:
            if -100 <= speed2 <= 100:
                sim_rspeed = speed2
        logging.info('SIM:go() lspeed={} rspeed={}'.format(sim_lspeed, sim_rspeed))
     




#IR Sensor Functions
def irLeft():
    """Returns state of Left IR Obstacle sensor."""
    irlx = sim_x - SIM_AXLE / 2 * sin(sim_direction) + SIM_FRONT * cos(sim_direction)
    irly = sim_y + SIM_AXLE / 2 * cos(sim_direction) + SIM_FRONT * sin(sim_direction)
    return sim_course.sim_atblock(irlx, irly)

def irRight():
    """Returns state of Right IR Obstacle sensor."""
    irrx = sim_x + SIM_AXLE / 2 * sin(sim_direction) + SIM_FRONT * cos(sim_direction)
    irry = sim_y - SIM_AXLE / 2 * cos(sim_direction) + SIM_FRONT * sin(sim_direction)
    return sim_course.sim_atblock(irrx, irry)

def irAll():
    """Returns true if any of the Obstacle sensors are triggered."""
    return irLeft or irRight

def irLeftLine():
    """Returns state of Left IR Line sensor.

    False if Black"""
    #sim_x, sim_y are centre of robot between axles.
    irlx = sim_x - SIM_GAP / 2 * sin(sim_direction) + SIM_FRONT * cos(sim_direction)
    irly = sim_y + SIM_GAP / 2 * cos(sim_direction) + SIM_FRONT * sin(sim_direction)
    return not sim_course.sim_online(irlx, irly)

def irRightLine():
    """Returns state of Right IR Line sensor.

    False if Black"""
    #sim_x, sim_y are centre of robot between axles.
    irrx = sim_x + SIM_GAP / 2 * sin(sim_direction) + SIM_FRONT * cos(sim_direction)
    irry = sim_y - SIM_GAP / 2 * cos(sim_direction) + SIM_FRONT * sin(sim_direction)
    return not sim_course.sim_online(irrx, irry)

# UltraSonic Functions
def getDistance():
    """Returns the distance in cm to the nearest block object.
    Distance is from sensors on front of robot.
    return distance or 0 if no object."""
    logging.debug('SIM:getDistance() called.')
    sensx = sim_x + SIM_FRONT * cos(sim_direction)
    sensy = sim_y + SIM_FRONT * sin(sim_direction)
    return sim_course.sim_getdistance(sensx, sensy, sim_direction)


""" Light Sensor Functions
(Full Pi2Go only)"""
def getLight(Sensor):
    """Returns the value 0..1023 for the selected sensor, 0 <= Sensor <= 3"""
    raise NotImplementedError

def getLightFL():
    """Returns the value 0..1023 for Front-Left light sensor"""
    raise NotImplementedError

def getLightFR():
    """Returns the value 0..1023 for Front-Right light sensor"""
    raise NotImplementedError

def getLightBL():
    """Returns the value 0..1023 for Back-Left light sensor"""
    raise NotImplementedError

def getLightBR(): 
    """Returns the value 0..1023 for Back-Right light sensor"""
    raise NotImplementedError


# Servo Functions
def startServos():
    """Initialises the servo background process."""
    raise NotImplementedError

def stopServos():
    """terminates the servo background process."""
    raise NotImplementedError

def setServo(Servo, Degrees):
    """Sets the servo to position in degrees -90 to +90."""
    raise NotImplementedError

def getSwitch():
    #getch
    return False
