#!/usr/bin/python

class ValueTree(object):

	def __init__(self, root, numState):
		self.root = ValueNode('root')
		self.numState = numState

	''' 
	insert the given list into the tree
	'''
	def insert(self, data):
		if(len(data)!=self.numState+2):
			print("Inappropriate data!")
		else
			self.root.makeBranch(data)

	'''
	Find the branch with given data and return the value at the end
	'''
	def find(self, data):
		if(len(data)!=self.numState+1):
			print("Not enough values given to find!")
			return None
		else
			return self.root.searchBranch(data)

	def update(self, value):
		pass



class ValueNode(object):

	'''
	initialize new node object
	value : value of the node
	child : list containing the children of the node. 
	'''
	def __init__(self, value):
		self.children = []
		self.value = value

	'''
	add(child_node):
	adds given child node into the tree structure
	child_node : ValueNode to be added into children list
	'''
	def addNode(self, child_node):
		self.children.append(child_node)

	def makeBranch(self, data):
		if(len(data)>1):
			childNode = self.searchChild(data[0])
			if(chidlNode==None):
				childNode = ValueNode(data[0])
				self.addNode(chidlNode)
			childNode.makeBranch(data[1:-1])
		if(len(data)==1):
			if(len(self.children)>1):
				print("Error! incorrect branch made")
			else if(len(self.children)==1):
				self.children[0].updateVal(data[0])
			else:
				selef.add(ValueNode(data[0]))


	def searchBranch(self, data):
		if(len(data)==1):
			if(self.searchChild(data[0])==None): return None
			else: return self.searchChild(data[0]).children[0].value
		if(len(data)>1):
			childNode = self.searchChild(data[0])
			if(chidlNode==None):
				return None
			if(len(data)>1):	
				childNode.searchBranch(data[1:-1])

	''' 
	changeVal(newVal)
	Changes the value of the node with the new given newVal
	newVal : new value of the node. Type int, float, string, etc
	'''
	def changeVal(self, newVal):
		self.value = newVal

	'''
	update the current value using the new value according to the defined value update rule
	'''
	def updateVal(self, newVal):
		#  TODO: add the value update method
		self.value = self.value + newVal

	'''
	Searchs for the child with given value. return None if not found
	'''
	def searchChild(self, value):
		# self.quickSearch(self.child)
		for i in range(len(self.children)):
			if(self.children[i].value == value):
				return self.children[i]
		return None

	'''
	quick search of given list
	'''
	def quickSearch(self, list):
		return None # TODO: dummy code to be replaced
