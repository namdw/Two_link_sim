#!/usr/bin/python

"""
	from TwoLink_sim import *

	place the TwoLink_sim.py in the working folder and 
	import the simulator as above to use


	list of current function

	TwoLink() : create the object
	move_link1(x) : move link 1 in x radians
	move_link2(x) : move link 2 in x radians
	getAngles(x) : return array of current joint angles in radians

	examples are below

	2016/08/20
	dnjsxodp@gmail.com
"""

from TwoLink_sim import * # add this linke to use the simulator
import time

cntrl_freq = 100

# Create the simulator object
sim = TwoLink()
# Start and display the Simulator graphics
sim.show()

time.sleep(1)
sim.move_link1(1)

time.sleep(0.5)
sim.randPoint()

time.sleep(1)
print('lets move')
for i in range(1*cntrl_freq):
	# Command the first link to move delta_angle
	sim.move_link1(3/cntrl_freq)
	time.sleep(1/cntrl_freq)
print('moved 1', sim.getAngles()) # get the current angle values (in radians)
print(sim.getEndpoint())

time.sleep(1)
for i in range(1*cntrl_freq):
	sim.move_link2(2/cntrl_freq)
	time.sleep(1/cntrl_freq)
print('moved 2', sim.getAngles())

time.sleep(1)
for i in range(1*cntrl_freq):
	sim.move_link1(-3/cntrl_freq)
	sim.move_link2(-2/cntrl_freq)
	time.sleep(1/cntrl_freq)
print('moved 1&2', sim.getAngles())