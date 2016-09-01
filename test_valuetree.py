#!/usr/bin/python

'''
tree class test function

test the tree and the node and make sure there is no error
'''
from ValueTree import *
import random

numState = 4
dataTree = ValueTree(numState)
# create random lists to be inserted into the tree
dataPool = []

for i in range(5):
	dataPool.append((numState+2)*[random.randint(1,5)])
print(dataPool)

for i in range(len(dataPool)):
	dataTree.insert(dataPool[i])

print(dataTree)

for i in range(len(dataTree.root.children)):
	print(dataTree.root.children[i].value)

for i in range(len(dataPool)):
	value = dataTree.find(dataPool[i][0:-1])
	print(value)