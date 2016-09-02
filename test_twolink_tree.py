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
import numpy as np
import random
from ValueTree import *
import math

# Variables
tryNumber = range(1,1,100) # how many try
cntrl_freq = 100
goal = [400,450]

epsilon = 0.5
actionList = []
actionX = range(-3,4)
actionY = range(-3,4)
for x in actionX:
	for y in actionY:
		actionList.append([x,y])
numState = 4
q_tree = ValueTree(numState)


# Function
def getAction(state):
	# valList = np.zeros(len(actionList))
	valList = []
	for i in range(len(actionList)):
		currentQset = [state[0], state[1], state[2], state[3], actionList[i]]
		value = q_tree.find(currentQset)
		if(value == None): value = float('-inf')
		valList.append(value)
	indices = [i for i, x in enumerate(valList) if x == max(valList)]
	return actionList[random.choice(indices)]


def egreedyExplore(state):
	if random.random() < epsilon:
		return random.choice(actionList)

	else:
		return getAction(state)


# def main():
# Create the simulator object
sim = TwoLink()

# Start and display the Simulator graphics
sim.show()
sim.makeGoal(goal)

time.sleep(1)


# e greedy exploration

# Add q value calculation here !!!

# temporary QA pair

print('lets move')
for i in range(10):
	# Command the first link to move delta_angle

	sim.move_link1(0.5/cntrl_freq)
	sim.move_link2(-1/cntrl_freq)


	angle = sim.getAngles()
	pos = sim.getPos()
	state = sim.getState()
	reward = sim.getReward(goal)

	action = [0.5,-1]
	currentQvalue = reward

	currentQset = [state[0], state[1], state[2], state[3], action, currentQvalue]

	# Update QvalueMatrix
	q_tree.insert(currentQset)

	time.sleep(1/cntrl_freq)


print('lets move2')
for i in range(10):
	# Command the first link to move delta_angle
	sim.move_link1(-0.5/cntrl_freq)
	sim.move_link2(1/cntrl_freq)

	angle = sim.getAngles()
	pos = sim.getPos()
	state = sim.getState()
	reward = sim.getReward(goal)

	action = [-0.5,1]
	currentQvalue = reward

	currentQset = [state[0], state[1], state[2], state[3], action, currentQvalue]

	# Update QvalueMatrix
	q_tree.insert(currentQset)

	time.sleep(1/cntrl_freq)


# print(q_tree.root.children)

for i in range(1000):
	# Command the first link to move delta_angle
	state = sim.getState()
	reward = sim.getReward(goal)
	action = egreedyExplore(state)

	currentQset = [state[0], state[1], state[2], state[3], action, reward]

	# Update QvalueMatrix
	q_tree.insert(currentQset)

	sim.move_link1(action[0]/cntrl_freq)
	sim.move_link2(action[1]/cntrl_freq)

	time.sleep(1/cntrl_freq)


# if __name__ == '__main__':
#     sys.exit(main())