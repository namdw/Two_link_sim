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
goal = [150,30]
ln_rate = 0.8
fg_rate = 0.8
currentQvalue = 0
flag = 0
epsilon = 0.1
actionList = np.array(range(-3,-4))

# Functions
def getQList(mat, state):
	dsize = np.shape(mat)

	for d in range(0,dsize[0]):
		if np.all(mat[d,0,:4] == state): # search state
			Qlist = [mat[d,0,5], mat[d,1,5], mat[d,2,5], mat[d,3,5]]

	return Qlist

def chooseAction(QList):

	dsize = np.shape(QList)

	maxQ = max(QList)
	count = QList.count(maxQ)

	if count > 1:
		i = 0
		for d in range(0,dsize[0]):
			if maxQ == QList[d]:
				chosenActionList[i] = d
				i = i + 1
		chosenAction = random.choice(chosenActionList)

	else:
		for d in range(0,dsize[0]):
			if maxQ == QList[d]:
				chosenAction = d

	return chosenAction

def egreedyExploration(QList):

	if random.random() < epsilon:
		egreedyChosenAction = random.choice(actionList)

	else:
		egreedyChosenAction = chooseAction(QList)

	return egreedyChosenAction










# Create the simulator object
sim = TwoLink()

# Start and display the Simulator graphics
sim.show()

time.sleep(1)


# e greedy exploration

# Add q value calculation here !!!

# temporary QA pair

print(q_3dmat)

print('lets move')
for i in range(100):
	# Command the first link to move delta_angle

	sim.move_link1(0.5/cntrl_freq)
	sim.move_link2(-1/cntrl_freq)


	angle = sim.getAngles()
	pos = sim.getPos()
	state = sim.getState()
	reward = sim.getReward(goal)

	action = 0
	currentQvalue = 0

	currentQset = np.array([state[0], state[1], state[2], state[3], action, currentQvalue])

	# Update QvalueMatrix
	q_tree.insert(currentQset)

	time.sleep(2/cntrl_freq)


print('lets move2')
for i in range(100):
	# Command the first link to move delta_angle
	sim.move_link1(-0.5/cntrl_freq)
	sim.move_link2(1/cntrl_freq)

	angle = sim.getAngles()
	pos = sim.getPos()
	state = sim.getState()
	reward = sim.getReward(goal)

	action = 0
	currentQvalue = 0

	currentQset = np.array([state[0], state[1], state[2], state[3], action, currentQvalue])

	# Update QvalueMatrix
	q_tree.insert(currentQset)

	time.sleep(2/cntrl_freq)


print(q_tree.root.children)
