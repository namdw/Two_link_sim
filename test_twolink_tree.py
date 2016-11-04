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
numTrain = 10
cntrl_freq = 100
goal = [150,100]

epsilon = 0.1
actionList = []
actionX = range(-2,3)
actionY = range(-2,3)
actionList = actionX
# for x in actionX:
# 	for y in actionY:
# 		actionList.append([x,y])
valList = len(actionList)*[0]
numState = 3
filename1 = "pretest_tree_set1.p"
filename2 = "pretest_tree_set2.p"
# filename3 = "pretest_tree_set3.p"
if os.path.isfile(filename1):
	f = open(filename1,'rb')
	q_tree1 = pickle.load(f)
	f.close()
else:
	q_tree1 = ValueTree(numState)

if os.path.isfile(filename2):
	f = open(filename2,'rb')
	q_tree2 = pickle.load(f)
	f.close()
else:
	q_tree2 = ValueTree(numState)

# if os.path.isfile(filename3):
# 	f = open(filename,'rb')
# 	q_tree3 = pickle.load(f)
# 	f.close()
# else:
# 	q_tree3 = ValueTree(numState)



# Function
def getAction(tree, state):
	# valList = np.zeros(len(actionList))
	for i in range(len(actionList)):
		# currentQset = [state[0], state[1], actionList[i]]
		currentQset = list(state)
		currentQset.append(actionList[i])
		value = tree.find(currentQset)
		if(value == None): value = float('-inf')
		# if(value == None): value = 0
		valList[i] = value
	indices = [i for i, x in enumerate(valList) if x == max(valList)]
	maxIndex = random.choice(indices)
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
		# action = egreedyExplore(q_tree, [state[0], state[1], sim.getGoalDist()])
		action1 = egreedyExplore(q_tree1, [state[0], state[1], sim.getHorz()])
		action2 = egreedyExplore(q_tree2, [state[0], state[1], sim.getVert()])
		stateVal = sim.getStateVal()
		# sim.move_link1(round(mean([action[0], action2[0], action3[0]]))/cntrl_freq)
		# sim.move_link2(round(mean([action[1], action2[1], action3[1]]))/cntrl_freq)
		# sim.move_link1(round(sum([action[0], action2[0], action3[0]]))/cntrl_freq)
		# sim.move_link2(round(sum([action[1], action2[1], action3[1]]))/cntrl_freq)
		sim.move_link1(action1/cntrl_freq)
		reward1 = sim.getStateVal()-stateVal
		stateVal = sim.getStateVal()
		sim.move_link2(action2/cntrl_freq)
		reward2 = sim.getStateVal()-stateVal
		time.sleep(1/cntrl_freq)
		
		# if action1!=0:
		# 	reward = reward-0.1
		# if action2!=0:
		# 	reward = reward-0.1

		## Global ACtion Control
		# currentQset = [state[0], state[1], sim.getGoalDist(), action, reward]

		# # Update QvalueMatrix
		# q_tree.insert(currentQset)

		# #test invQ methods
		# state = sim.getState()
		# invQset = [state[0], state[1], [-1*action[0],-1*action[1]], sim.getGoalDist(), -1*reward]
		# q_tree.insert(invQset)

		## Link 1 ACtion Control
		currentQset = [state[0], state[1], sim.getHorz(), action1, reward1]

		# Update QvalueMatrix
		q_tree1.insert(currentQset)

		#test invQ methods
		state = sim.getState()
		invQset = [state[0], state[1], sim.getHorz(), -1*action1, -1*reward1]
		q_tree1.insert(invQset)

		## Link 2 Action Control
		currentQset = [state[0], state[1], sim.getVert(), action2, reward2]
		# Update QvalueMatrix
		q_tree2.insert(currentQset)

		#test invQ methods
		state = sim.getState()
		invQset = [state[0], state[1], sim.getVert(), -1*action2, -1*reward2]
		q_tree2.insert(invQset)


print("done exploring")

f = open(filename1,'wb')
pickle.dump(q_tree1,f)
f.close()
f = open(filename2,'wb')
pickle.dump(q_tree2,f)
f.close()
# f = open(filename3,'wb')
# pickle.dump(q_tree3,f)
# f.close()
print("done with pickle")

# if __name__ == '__main__':
#     sys.exit(main())