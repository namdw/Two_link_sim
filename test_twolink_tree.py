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
import pickle
import os.path

# Variables
# tryNumber = range(1,1,100) # how many try
numTrain = 5
cntrl_freq = 100
goal = [150,100]

epsilon = 0.2
actionList = []
actionX = range(-3,4)
actionY = range(-3,4)
for x in actionX:
	for y in actionY:
		actionList.append([x,y])
valList = len(actionList)*[0]
numState = 3
filename = "pretest_tree_set1.p"
filename2 = "pretest_tree_set2.p"
filename3 = "pretest_tree_set3.p"
if os.path.isfile(filename):
	f = open(filename,'rb')
	q_tree = pickle.load(f)
	f.close()
else:
	q_tree = ValueTree(numState)

if os.path.isfile(filename2):
	f = open(filename,'rb')
	q_tree = pickle.load(f)
	f.close()
else:
	q_tree2 = ValueTree(numState)

if os.path.isfile(filename3):
	f = open(filename,'rb')
	q_tree = pickle.load(f)
	f.close()
else:
	q_tree3 = ValueTree(numState)



# Function
def getAction(tree, state):
	# valList = np.zeros(len(actionList))
	for i in range(len(actionList)):
		# currentQset = [state[0], state[1], actionList[i]]
		currentQset = list(state)
		currentQset.append(actionList[i])
		value = tree.find(currentQset)
		if(value == None): value = float('-inf')
		valList[i] = value
	indices = [i for i, x in enumerate(valList) if x == max(valList)]
	maxIndex = random.choice(indices)
	# print(valList[maxIndex])
	return actionList[maxIndex]


def egreedyExplore(tree, state):
	if random.random() < epsilon:
		# print('random choice')
		return random.choice(actionList)

	else:
		return getAction(tree, state)

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

# def main():
# Create the simulator object
sim = TwoLink()

# Start and display the Simulator graphics
sim.show()
# sim.randGoal()

time.sleep(1)


# e greedy exploration

# Add q value calculation here !!!

# temporary QA pair

# print('lets move')
# for i in range(10):

# 	pos = sim.getEndpoint()
# 	state = sim.getState()
# 	stateVal = sim.getStateVal()
# 	sim.move_link1(0.5/cntrl_freq)
# 	sim.move_link2(-1/cntrl_freq)
# 	time.sleep(1/cntrl_freq)
# 	reward = sim.getStateVal()-stateVal

# 	action = [0.5,-1]
# 	currentQvalue = reward

# 	# currentQset = [state[0], state[1], action, currentQvalue]
# 	currentQset = list(state)
# 	currentQset.append(action)
# 	currentQset.append(currentQvalue)

# 	# Update QvalueMatrix
# 	# q_tree.insert(currentQset)



# print('lets move2')
# for i in range(10):

# 	pos = sim.getEndpoint()
# 	state = sim.getState()
# 	stateVal = sim.getStateVal()
# 	sim.move_link1(-0.5/cntrl_freq)
# 	sim.move_link2(1/cntrl_freq)
# 	time.sleep(1/cntrl_freq)
# 	reward = sim.getStateVal()-stateVal

# 	action = [-0.5,1]
# 	currentQvalue = reward

# 	# currentQset = [state[0], state[1], action, currentQvalue]
# 	currentQset = state
# 	currentQset.append(action)
# 	currentQset.append(currentQvalue)

# 	# Update QvalueMatrix
# 	# q_tree.insert(currentQset)


for numTry in range(numTrain):
	sim.reset()
	# sim.makeGoal(goal)
	sim.randGoal()
	for i in range(500):
		# Command the first link to move delta_angle
		state = sim.getState()
		action = egreedyExplore(q_tree, [state[0], state[1], sim.getGoalDist()])
		action2 = egreedyExplore(q_tree2, [state[0], state[1], sim.getVert()])
		action3 = egreedyExplore(q_tree3, [state[0], state[1], sim.getHorz()])
		stateVal = sim.getStateVal()

		sim.move_link1(round(mean([action[0], action2[0], action3[0]]))/cntrl_freq)
		sim.move_link2(round(mean([action[1], action2[1], action3[1]]))/cntrl_freq)
		time.sleep(1/cntrl_freq)
		
		reward = sim.getStateVal()-stateVal
		
		currentQset = [state[0], state[1], sim.getGoalDist(), action, reward]

		# Update QvalueMatrix
		q_tree.insert(currentQset)

		#test invQ methods
		state = sim.getState()
		invQset = [state[0], state[1], [-1*action[0],-1*action[1]], sim.getGoalDist(), -1*reward]
		q_tree.insert(invQset)

		currentQset = [state[0], state[1], sim.getVert(), action2, reward]
		# Update QvalueMatrix
		q_tree2.insert(currentQset)

		#test invQ methods
		state = sim.getState()
		invQset = [state[0], state[1], sim.getVert(), [-1*action2[0],-1*action2[1]], -1*reward]
		q_tree2.insert(invQset)

		currentQset = [state[0], state[1], sim.getHorz(), action3, reward]

		# Update QvalueMatrix
		q_tree3.insert(currentQset)

		#test invQ methods
		state = sim.getState()
		invQset = [state[0], state[1], sim.getHorz(), [-1*action3[0],-1*action3[1]], -1*reward]
		q_tree3.insert(invQset)

print("done exploring")

f = open(filename,'wb')
pickle.dump(q_tree,f)
f.close()
f = open(filename2,'wb')
pickle.dump(q_tree,f)
f.close()
f = open(filename3,'wb')
pickle.dump(q_tree,f)
f.close()
print("done with pickle")

# if __name__ == '__main__':
#     sys.exit(main())