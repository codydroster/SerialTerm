#!/usr/bin/env python


import window

import threading
import time
import serial
import pygame
import sys
from multiprocessing import Process, Manager
from gi.repository import Gtk, Gdk, GLib, GObject

mainwin = window.MainWindow()


def app_main():



	mainwin.connect("destroy", Gtk.main_quit)
	pygame.display.init()

	#Gdk.threads_init()
	GObject.threads_init()
	#GLib.threads_init()
	Gdk.threads_enter()


	thread1.start()
#	thread2.start()

	GObject.idle_add(update_gui)
	GObject.timeout_add(1, serialbg)

	window.Gtk.main()
	Gdk.threads_leave();
	pygame.quit()




def background():
	pygame.joystick.init()
	tbuf = mainwin.scrolled_term.term_text.get_buffer()
	contbox = mainwin.appmenu.controllerwin.controllerbox

	joystickid = mainwin.appmenu.controllerwin.controllerbox.contcombo.get_active()

	while(joystickid is -1):
		joystickid = mainwin.appmenu.controllerwin.controllerbox.contcombo.get_active()


	joystickinuse = pygame.joystick.Joystick(joystickid)
	joystickinuse.init()

	#Window Terminal

	mainwin.scrolled_term.insert_text_term('Connected: ' + joystickinuse.get_name())
	contbox.butbox.joystick = joystickinuse

	while(True):
		joystickid = mainwin.appmenu.controllerwin.controllerbox.contcombo.get_active()



		pygame.event.pump()


	#main code
		if joystickinuse.get_id() == joystickid:
			buttonattr = contbox.butbox.buttonattr			
			axisattr = contbox.butbox.axisattr
			hatattr = contbox.butbox.hatattr

			values = mainwin.values
			entryarray = mainwin.appmenu.controllerwin.controllerbox.bytebox.entryarray

			for i, button in enumerate(buttonattr[joystickinuse.get_id()]):
				button.rawvalue = joystickinuse.get_button(i)
				button.buttoncnt += button.get_value()

			for i, axis in enumerate(axisattr[joystickinuse.get_id()]):
				axis.rawvalue = joystickinuse.get_axis(i)


			for i in range(joystickinuse.get_numhats()):
				
				value = joystickinuse.get_hat(i)	#get hat i: joystick inuse
				valuex = value[0]
				valuey = value[1]

				hatattr[joystickinuse.get_id()][i].rawvalue = valuex
				hatattr[joystickinuse.get_id()][i+1].rawvalue = valuey

				hatattr[joystickinuse.get_id()][i].buttoncnt += hatattr[joystickinuse.get_id()][i].get_value()
				hatattr[joystickinuse.get_id()][i+1].buttoncnt += hatattr[joystickinuse.get_id()][i+1].get_value()

	#array to store values - not formatted into byte array
			

			for i in range(len(entryarray)):
				buttoncount = 0
				axisval = 0
				constval = 0

				if len(values) < (i+1):
					values.append(0)
					
				if hasattr(entryarray[i], 'byteval'):
					constval = entryarray[i].byteval

				if hasattr(entryarray[i], 'button0'):
					if entryarray[i].button0 != None:
						buttoncount = buttonattr[joystickinuse.get_id()][entryarray[i].button0].buttoncnt 
					if entryarray[i].button1 != None:
						buttoncount +=	buttonattr[joystickinuse.get_id()][entryarray[i].button1].buttoncnt
					
					

				if hasattr(entryarray[i], 'hat'):
					if entryarray[i].hat != None:
						buttoncount = hatattr[joystickinuse.get_id()][entryarray[i].hat].buttoncnt 
					
	
				if hasattr(entryarray[i], 'axis'):
					if entryarray[i].axis !=None:
						axisval = axisattr[joystickinuse.get_id()][entryarray[i].axis].value
						
	
				values[i] =  buttoncount + axisval + constval
						
				print(int(values[i]))				
	
#		for val in mainwin.values:
#				print(val)



			

		elif joystickid != -1:
			
			joystickinuse = pygame.joystick.Joystick(joystickid)
			mainwin.scrolled_term.insert_text_term('Connected: ' + joystickinuse.get_name())
			contbox.butbox.joystick = joystickinuse


					
def update_gui():
	joystickid = mainwin.appmenu.controllerwin.controllerbox.contcombo.get_active()
	
	if joystickid != -1:
		joystickinuse = pygame.joystick.Joystick(joystickid)
		buttonattr = mainwin.appmenu.controllerwin.controllerbox.butbox.buttonattr
		axisattr = mainwin.appmenu.controllerwin.controllerbox.butbox.axisattr
		hatattr = mainwin.appmenu.controllerwin.controllerbox.butbox.hatattr

		for i, button in enumerate(buttonattr[joystickinuse.get_id()]):
			button.set_levelbar(button.get_value())
		for i, axis in enumerate(axisattr[joystickinuse.get_id()]):
			axis.set_levelbar(axis.get_value())

		for i in range(joystickinuse.get_numhats()):
			hatattr[joystickinuse.get_id()][i].set_levelbar(hatattr[joystickinuse.get_id()][i].get_value())
			hatattr[joystickinuse.get_id()][i+1].set_levelbar(hatattr[joystickinuse.get_id()][i+1].get_value())
		


	return True



def serialbg():
	joystickid = mainwin.appmenu.controllerwin.controllerbox.contcombo.get_active()
	entryarray = mainwin.appmenu.controllerwin.controllerbox.bytebox.entryarray
	buttonattr = mainwin.appmenu.controllerwin.controllerbox.butbox.buttonattr
	axisattr = mainwin.appmenu.controllerwin.controllerbox.butbox.axisattr
	hatattr = mainwin.appmenu.controllerwin.controllerbox.butbox.hatattr

	port = mainwin.serialportbox.useport

	transmitbytes = []

	if joystickid != -1:
		joystickinuse = pygame.joystick.Joystick(joystickid)

		for bytes in entryarray:
			if bytes.numbytes == 1:
				if hasattr(bytes, 'axiscombo'):
					None
				else:
					None	

			if bytes.numbytes == 2:
				None






	#format bytestruct and controller values here

#	while(True):
	if(port.is_open):
		if(port.out_waiting == 0):
			port.write(transbytes)
	return True





thread1 = threading.Thread(target=background)
thread1.daemon = True

#thread2 = threading.Thread(target=serialbg)
#thread2.daemon = True



app_main()





