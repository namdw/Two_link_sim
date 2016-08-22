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
	

	2016/08/20
	dnjsxodp@gmail.com
"""

from tkinter import *
from tkinter import ttk
import time
import threading
from math import *


# def _create_circle(self, x, y, r, **kwargs):
# 	return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

ground_pos = (300,300)
joint_pos = (0,0)
gripper_pos = (0,0)
link1_len = 100
link2_len = 100
w = ''
link1 = ''
link2 = ''
joint = ''
gripper = ''
angle1 = 0
angle2 = 0
thread1 = ''
max_speed = 2
cntrl_freq = 100



class myThread(threading.Thread):
	def __init__(self, func):
		threading.Thread.__init__(self)
		self.func = func

	def run(self):
		self.func()


class TwoLink(object):
	def __init__(self):
		self.__run_control = False
		self.__root = ''
		self.angle1 = 0
		self.angle2 = 0
	
	def show(self):
		thread1 = myThread(self.show_sub)
		thread1.start()
		time.sleep(0.1)
		self.__run_control = True
		thread2 = myThread(self.controlLoop)
		thread2.start()

	def getAngles(self):
		return [self.angle1, self.angle2]

	def controlLoop(self):
		while(self.__run_control):
			if (self.__root==''): break
			self.redraw()
			time.sleep(1/cntrl_freq)
		print('End of while loop')

	def move_link1(self, delta_a):
		global angle1
		angle1 = angle1 + delta_a
		self.angle1 = angle1

	def move_link2(self, delta_a):
		global angle2 
		angle2 = angle2 + delta_a
		self.angle2 = angle2

	def redraw(self):
		global w, link1, link2, joint_pos, gripper_pos
		new_pos = (ground_pos[0] + link1_len * cos(self.angle1), ground_pos[1] - link1_len * sin(self.angle1))
		new_pos2 = (new_pos[0] + link2_len * cos(self.angle1+self.angle2), new_pos[1] - link2_len * sin(self.angle1+self.angle2))

		delta_x1 = new_pos[0]-joint_pos[0]
		delta_y1 = new_pos[1]-joint_pos[1]
		delta_x2 = new_pos2[0]-gripper_pos[0]
		delta_y2 = new_pos2[1]-gripper_pos[1]

		w.delete('link')
		
		w.move(joint, delta_x1, delta_y1)
		w.move(gripper, delta_x2, delta_y2)
		joint_pos = new_pos
		gripper_pos = new_pos2
		link1 = w.create_line(ground_pos[0], ground_pos[1], new_pos[0], new_pos[1], tags='link')
		link2 = w.create_line(new_pos[0], new_pos[1], new_pos2[0], new_pos2[1], tags='link')

	def show_sub(self):
		global joint_pos, gripper_pos, w, link1, link2, joint, gripper, root
		if (self.__root==''):
			self.__root = Tk()
			self.__root.title = "Two Link Arm Simulator"
			self.__root.geometry('620x620')
			self.__root.resizable(FALSE, FALSE)

			mainframe = ttk.Frame(self.__root, padding="10 10 10 10")
			mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

			w = Canvas(mainframe, width=600, height=600)
			w.config(bg='gray')
			w.grid(row=0,column=0)

			node_r = 10

			ground = w.create_oval(ground_pos[0]-10, ground_pos[1]-node_r, ground_pos[0]+node_r, ground_pos[1]+node_r, fill='red', outline='red')
			joint_pos = (ground_pos[0] + link1_len * cos(angle1), ground_pos[1] + link1_len * sin(angle2))
			joint = w.create_oval(joint_pos[0]-node_r, joint_pos[1]-node_r, joint_pos[0]+node_r, joint_pos[1]+node_r, fill='red', outline='red')
			gripper_pos = (joint_pos[0] + link2_len * cos(angle1+angle2), joint_pos[1] + link2_len * sin(angle1+angle2))
			gripper = w.create_oval(gripper_pos[0]-node_r, gripper_pos[1]-node_r, gripper_pos[0]+node_r, gripper_pos[1]+node_r, fill='red', outline='red')
			
			link1 = w.create_line(ground_pos[0], ground_pos[1], joint_pos[0], joint_pos[1], tags='link')
			link2 = w.create_line(joint_pos[0], joint_pos[1], gripper_pos[0], gripper_pos[1], tags='link')
			self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)
			self.__root.mainloop()

	def on_closing(self):
		print('Going to exit now!')
		self.__run_control = False
		time.sleep(0.1)
		self.__root.destroy()
		self.__root = ''
