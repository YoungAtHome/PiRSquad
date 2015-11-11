#!/usr/bin/python3
# sim_linecourse.py
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

# curve parameters
#       ## ##
#     #       #
#   #           #
# #          0,0  #
# #  -20,0        #
#
# # -20,-20       #
# #        0,-20  #
#   #           #
#     #       #
#       ## ##
def sim_buildcurve(h,v,ho,vo):
	return lambda x, y: (0<=(x-h)<20) and (0<=(y-v)<20) and (9.5 < sqrt((x-h+ho)**2 + (y-v+vo)**2) < 10.5)


def sim_buildhline(h,v):
	"""Horizontal line builder
	"""
	return lambda x, y: (0<=(x-h)<20) and (0<=(y-v)<20) and (9.5 < (y-v) < 10.5)

def sim_buildvline(h,v):
	return lambda x, y: (0<=(x-h)<20) and (0<=(y-v)<20) and (9.5 < (x-h) < 10.5)
	
# line following course - simple rounded square
sim_line_segments = (sim_buildcurve(0,0,-20,-20), sim_buildhline(20,0), sim_buildcurve(40,0,0,-20), sim_buildvline(40,20),
	sim_buildcurve(40,40,0,0), sim_buildhline(20,40), sim_buildcurve(0,40,-20,0), sim_buildvline(0,20))

# three-point-turn course
# start line, cross line, mid line, left boundary, back boundary, right boundary
sim_3point_segments = (sim_buildhline(0,35), sim_buildhline(20,35), sim_buildhline(40,35), sim_buildhline(60,35), sim_buildhline(80,35), sim_buildhline(100,35), 
	sim_buildhline(0,150), sim_buildhline(20,150), sim_buildhline(40,150), sim_buildhline(60,150), sim_buildhline(80,150), sim_buildhline(100,150), 
	sim_buildhline(30,190), sim_buildhline(50,190), sim_buildhline(70,190), 
	sim_buildvline(10,160), sim_buildvline(10,180), sim_buildvline(10,200), sim_buildvline(10,220),
	sim_buildhline(0,230), sim_buildhline(20,230), sim_buildhline(40,230), sim_buildhline(60,230), sim_buildhline(80,230), sim_buildhline(100,230), 
	sim_buildvline(90,160), sim_buildvline(90,180), sim_buildvline(90,200), sim_buildvline(90,220))

# assign current course
#sim_course = sim_line_segments
sim_course = sim_3point_segments
				
def sim_online(x,y):
	"""Check if position is on the line
	
	Return boolean, True if on line, False otherwise
	"""
	sim_on = False
	for sim_Segment in sim_course:
		sim_on = sim_Segment(x,y)
		if sim_on: return sim_on
	return sim_on

def sim_test():
	"""Test the simulated course with diagonal lines
	"""
	for o in range(-5,6,5):
		for r in range(30):
			x = r+o
			y = 30-(r+o)
			print (x, " ", y, " ", sim_online(x,y))

if __name__ == "__main__":
	sim_test()

def sim_test3():
	"""Display the simulated course at resolution of steps
	"""
	for y in range(60,-1,-1):
		line = '{0:02d}'.format(y) + " "
		for x in range(0,61,1):
			if sim_online(x,y):
				line += "#"
			else:
				line += " "
		print (line)
		
if __name__ == "__main__":
	sim_test3()
	
def sim_test2():
	"""Test the simulated course with random positions
	"""
	for r in range(100):
		x = random.randrange(60)
		y = random.randrange(60)
		print (x, " ", y, " ", sim_online(x,y))

if __name__ == "__main__":
	sim_test2()
