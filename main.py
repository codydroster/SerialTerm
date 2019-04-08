


import window


import threading
import time
import serial
import pygame
import sys
from multiprocessing import Process, Manager
from gi.repository import Gtk, Gdk, GLib, GObject

mainwin = window.MainWindow()

valuesinbyte = bytearray()
entryarray = mainwin.appmenu.controllerwin.controllerbox.bytebox.entryarray

values = mainwin.values
port = mainwin.serialportbox.useport
bytes = []
def app_main():



	mainwin.connect("destroy", Gtk.main_quit)
	pygame.display.init()



	GLib.idle_add(update_gui)
	GLib.idle_add(background)

	GLib.timeout_add(15, serialbg)

	window.Gtk.main()
	
	pygame.quit()




def background():
	pygame.joystick.init()
	tbuf = mainwin.scrolled_term.term_text.get_buffer()
	contbox = mainwin.appmenu.controllerwin.controllerbox
	joystickid = mainwin.appmenu.controllerwin.controllerbox.contcombo.get_active()
	joystickinuse = mainwin.appmenu.controllerwin.controllerbox.joystick2
	
	joystickid = mainwin.appmenu.controllerwin.controllerbox.contcombo.get_active()


	if joystickid != -1:

		pygame.event.pump()
		
	#	print(joystickinuse.get_axis(1))
#main code

		if joystickinuse.get_id() == joystickid:
			buttonattr = contbox.butbox.buttonattr			
			axisattr = contbox.butbox.axisattr
			hatattr = contbox.butbox.hatattr


	
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

				if len(values) < (i + 1):
					values.append(0)
				
				if hasattr(entryarray[i], 'byteval'):
					constval = entryarray[i].byteval

				if hasattr(entryarray[i], 'button0'):
					if entryarray[i].button0 != None:
						buttoncount += buttonattr[joystickinuse.get_id()][entryarray[i].button0].buttoncnt 
					if entryarray[i].button1 != None:
						buttoncount +=	buttonattr[joystickinuse.get_id()][entryarray[i].button1].buttoncnt
				
				

				if hasattr(entryarray[i], 'hat'):
					if entryarray[i].hat != None:
						buttoncount = hatattr[joystickinuse.get_id()][entryarray[i].hat].buttoncnt 
				

				if hasattr(entryarray[i], 'axis'):
					if entryarray[i].axis !=None:
						axisval = axisattr[joystickinuse.get_id()][entryarray[i].axis].value
					

				values[i] = int(buttoncount + axisval + constval)
			


			
	return True


					
def update_gui():
	mainwin_vals = mainwin.bytevalbox.mainwin_vals
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
		
		
	#mainwin update
		if len(mainwin_vals) == len(values):
			for i, val in enumerate(mainwin_vals):

				val[1].set_text(str(values[i]))


		


	return True



def serialbg():

	transmit = bytearray()
	
	for i, byt in enumerate(values):

		if entryarray[i].numbytes == 1:
			transmit.append(byt)

		elif entryarray[i].numbytes == 2:
			transmit.append((byt >> 8) & 0xff)
			transmit.append(byt & 0xff)
	
	if port.is_open:
			
		port.write(transmit)
				

	return True




app_main()











