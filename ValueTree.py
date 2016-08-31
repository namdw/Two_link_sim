#!/usr/bin/python

class ValueNode():

	def __init__(self, value):
	'''
	initialize new node object
	value : value of the node
	child : list containing the children of the node. 
	'''
		self.children = {}
		self.value = value

	def add(self, child_node):
	'''
	adds given child node into the tree structure
	'''
		self.children.append(child_node)

	def changeValue(self, newVal):
	'''
	Changes the value of the node with the new given newVal
	'''
		self.value = newVal

	def searchChild(self, value):
	'''
	Searchs for the child with given value. return None if not found
	'''
		# self.quickSearch(self.child)
		for i in range(len(self.children)):
			if(self.children[i].value == value):
				return self.children[i]
		return None

	def quickSearch(self, list):
	'''
	quick search of given list
	'''
		return None # TODO: dummy code to be replaced

class ValueTree():

	def __init__(self, root, numState):
		self.root = root
		self.numState = numState

	def insert(self, data):
	''' 
	insert the given list into the tree
	'''
		if(len(data)!=self.numState+2):
			print("Inappropriate data!")
		else
			pass # TODO: do the insertion here

	def find(self, data):
	'''
	Find the branch with given data and return the value at the end
	'''
		if(len(data)!=self.numState+1):
			print("Not enough values given to find!")
			return None
		else
			return None # TODO: do the search and return the value