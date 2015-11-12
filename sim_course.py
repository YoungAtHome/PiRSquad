#!/usr/bin/python3
# sim_course.py
# PiWars 2015 Environment simulation code library
# Author: Nick Young

from math import sqrt
if __name__ == "__main__":
#just for testing
	import random

# describe the line following course
# use a series of limited equations
# Assumptions:
# Course is made of 20cm square sections with 90deg curves and 1cm wide lines.
SIM_LINE_WIDTH=1
SIM_TILE_SIZE=20

SIM_FREE=0
SIM_LINE=1
SIM_BLOCK=2

# curve parameters
#       ## ##
#     #       #
#   #           #
# #          0,0  #
# #  -1,0         #
#
# # -1,-1         #
# #        0,-1   #
#   #           #
#     #       #
#       ## ##
def sim_buildcurve(h,v,ho,vo):
	"""Curved line builder
	
	ho - horizontal offset is either 0 or -1
	vo - vertical offset is either 0 or -1
	
	0,0 - upward and left curve
	0,-1 - left and down curve
	-1,-1 - down and right curve
	-1,0 - right and up curve"""
	return lambda x, y: (0<=(x-h)<SIM_TILE_SIZE) and (0<=(y-v)<SIM_TILE_SIZE) and ((SIM_TILE_SIZE/2-SIM_LINE_WIDTH/2) < sqrt((x-h+(ho*SIM_TILE_SIZE))**2 + (y-v+(vo*SIM_TILE_SIZE)))**2) < (SIM_TILE_SIZE/2+SIM_LINE_WIDTH/2)) and SIM_LINE


def sim_buildhline(h,v):
	"""Horizontal line builder"""
	return lambda x, y: (0<=(x-h)<SIM_TILE_SIZE) and (0<=(y-v)<SIM_TILE_SIZE) and ((SIM_TILE_SIZE/2-SIM_LINE_WIDTH/2) < (y-v) < (SIM_TILE_SIZE/2+SIM_LINE_WIDTH/2)) and SIM_LINE

def sim_buildvline(h,v):
	return lambda x, y: (0<=(x-h)<SIM_TILE_SIZE) and (0<=(y-v)<SIM_TILE_SIZE) and ((SIM_TILE_SIZE/2-SIM_LINE_WIDTH/2) < (x-h) < (SIM_TILE_SIZE/2+SIM_LINE_WIDTH/2)) and SIM_LINE

def sim_buildblock(h1,v1,h2,v2):
	return lambda x, y: (h1<= x <h2) and (v1<= y <v2) and SIM_BLOCK
	
	
# stright line course - start line, stop line and two long walls	
sim_straight_segments = (sim_buildhline(0,20), sim_buildhline(20,20), sim_buildhline(40,20),
						sim_buildblock(0,0,2,240), sim_buildblock(58,0,60,240))
sim_stright_size = (60,240)
	
	
# line following course - simple rounded square	
sim_line_segments = (sim_buildcurve(0,0,-1,-1), sim_buildhline(20,0), sim_buildcurve(40,0,0,-1), sim_buildvline(40,20),
	sim_buildcurve(40,40,0,0), sim_buildhline(20,40), sim_buildcurve(0,40,-1,0), sim_buildvline(0,20))
sim_line_size = (60,60)
	
# three-point-turn course
# start line, cross line, mid line, left boundary, back boundary, right boundary
sim_3point_segments = (sim_buildhline(0,35), sim_buildhline(20,35), sim_buildhline(40,35), sim_buildhline(60,35), sim_buildhline(80,35), sim_buildhline(100,35), 
	sim_buildhline(0,150), sim_buildhline(20,150), sim_buildhline(40,150), sim_buildhline(60,150), sim_buildhline(80,150), sim_buildhline(100,150), 
	sim_buildhline(30,190), sim_buildhline(50,190), sim_buildhline(70,190), 
	sim_buildvline(10,160), sim_buildvline(10,180), sim_buildvline(10,200), sim_buildvline(10,220),
	sim_buildhline(0,230), sim_buildhline(20,230), sim_buildhline(40,230), sim_buildhline(60,230), sim_buildhline(80,230), sim_buildhline(100,230), 
	sim_buildvline(90,160), sim_buildvline(90,180), sim_buildvline(90,200), sim_buildvline(90,220))
sim_3point_size = (120,240)
	
# assign current course
#sim_course = sim_line_segments
#sim_course_size = sim_line_size
sim_course = sim_3point_segments
sim_course_size = sim_3point_size
#sim_course = sim_stright_segments
#sim_course_size = sim_stright_size


def sim_online(x,y):
	"""Check if position is on the line
	
	Return boolean, True if on line, False otherwise"""
	return sim_chk(x, y, SIM_LINE)
		
def sim_atblock(x,y):
	"""Check if position is at a block
	
	Return boolean, True if at block"""
	return sim_chk(x, y, SIM_BLOCK)

def sim_check(x,y,t):
	"""Check if position is onn a line or at a block
	
	Return boolean, True if on line or at block"""
	sim_chk = False
	for sim_Segment in sim_course:
		if sim_Segment(x,y) = t:
			sim_chk = True
			break
	return sim_chk

	
def sim_getDistance(x,y,dir):
	"""Get distance to next block
	
	Return boolean, True if at block"""
	return False
	

def sim_test():
	"""Test the simulated course with diagonal lines"""
	for o in range(-5,6,5):
		for r in range(30):
			x = r+o
			y = 30-(r+o)
			print (x, " ", y, " ", sim_online(x,y))

if __name__ == "__main__":
	sim_test()

def sim_test3():
	"""Display the simulated course at resolution of steps"""
	for y in range(sim_course_size[1],-1,-1):
		course = '{0:02d}'.format(y) + " "
		for x in range(0,sim_course_size[0]+1,1):
			if sim_online(x,y):
				course += "#"
			elis sim_atblock(x,y):
				course += "@"
			else:
				course += " "
		print (course)
		
if __name__ == "__main__":
	sim_test3()
	
def sim_test2():
	"""Test the simulated course with random positions"""
	for r in range(100):
		x = random.randrange(sim_course_size[0])
		y = random.randrange(sim_course_size[1])
		print (x, " ", y, " ", sim_check(x,y))

if __name__ == "__main__":
	sim_test2()
