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

# Variables
tryNumber = range(1,1,100) # how many try
cntrl_freq = 100
goal = [150,30]
ln_rate = 0.8
fg_rate = 0.8
currentQvalue = 0
flag = 0
epsilon = 0.1
actionList = np.array([0,1,2,3])
# 0: 1axis -1 step, 1: 1axis +1 step, 2: 2axis -1 step, 3: 2axis +1 step
q_3dmat = np.array([[[0.0,0.0,0.0,0.0,0,0.0], 
	                 [0.0,0.0,0.0,0.0,1,0.0],
	                 [0.0,0.0,0.0,0.0,2,0.0],
	                 [0.0,0.0,0.0,0.0,3,0.0]],
	                [[0.0,0.0,0.0,0.0,0,0.0],
	                 [0.0,0.0,0.0,0.0,1,0.0],
	                 [0.0,0.0,0.0,0.0,2,0.0],
	                 [0.0,0.0,0.0,0.0,3,0.0]]]) 
# make 3d array for state,action,value set 
# q_3dmat[0,0] = [link1State, link2State, posxState, posyState, action, QValue]

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

	epsilon = 0.1
	actionList = [0,1,2,3]

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

# Initialize !!!
#----------------------------------------------------------------------------------------------------
angle = sim.getAngles()
pos = sim.getPos()
state = sim.getState()
reward = sim.getReward(goal)

action = 0
currentQvalue = 0

currentQset = np.array([state[0], state[1], state[2], state[3], action, currentQvalue])

# Init QvalueMatrix
dsize = np.shape(q_3dmat)

for d in range(0,dsize[0]):
	if np.all(q_3dmat[d,0,:4] == currentQset[:4]): # search state
		flag = 1
		depth = d

if flag == 1:
	for c in range(0,dsize[1]):
		if q_3dmat[depth,c,4] == currentQset[4]: # search action
			q_3dmat[depth,c] = currentQset
			flag = 0
else: 
	newQAset = np.array([currentQset, currentQset, currentQset, currentQset])
	newQAset[:,4] = actionList
	newQAset[:,5] = 0
	newQAset[action,5] = currentQvalue
	q_3dmat = np.concatenate((q_3dmat,[newQAset]), axis = 0)
#---------------------------------------------------------------------------------------------------------



# e greedy exploration

# Add q value calculation here !!!

# temporary QA pair

print(q_3dmat)

print('lets move')
for i in range(10):
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
	dsize = np.shape(q_3dmat)
	
	for d in range(0,dsize[0]):
		print(d)
		if np.all(q_3dmat[d,0,:4] == currentQset[:4]): # search state
			print("Find state!!!!")
			flag = 1
			depth = d

	if flag == 1:
		for c in range(0,dsize[1]):
			if q_3dmat[depth,c,4] == currentQset[4]: # search action
				q_3dmat[depth,c] = currentQset
				flag = 0
	else: 
		newQAset = np.array([currentQset, currentQset, currentQset, currentQset])
		newQAset[:,4] = actionList
		newQAset[:,5] = 0
		newQAset[action,5] = currentQvalue
		q_3dmat = np.concatenate((q_3dmat,[newQAset]), axis = 0)

	time.sleep(2/cntrl_freq)


print('lets move2')
for i in range(10):
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
	dsize = np.shape(q_3dmat)
	
	for d in range(0,dsize[0]):
		print(d)
		if np.all(q_3dmat[d,0,:4] == currentQset[:4]): # search state
			print("Find state!!!!")
			flag = 1
			depth = d

	if flag == 1:
		for c in range(0,dsize[1]):
			if q_3dmat[depth,c,4] == currentQset[4]: # search action
				q_3dmat[depth,c] = currentQset
				flag = 0
	else: 
		newQAset = np.array([currentQset, currentQset, currentQset, currentQset])
		newQAset[:,4] = actionList
		newQAset[:,5] = 0
		newQAset[action,5] = currentQvalue
		q_3dmat = np.concatenate((q_3dmat,[newQAset]), axis = 0)

	time.sleep(2/cntrl_freq)

print(q_3dmat)
