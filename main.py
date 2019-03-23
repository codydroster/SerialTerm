#!/usr/bin/env python


import window
import threading
import time
import serial
import pygame
import sys
from multiprocessing import Process, Manager
from gi.repository import Gtk, Gdk, GLib

mainwin = window.MainWindow()
joystickid = mainwin.appmenu.controllerwin.controllerbox.contcombo.get_active()


def app_main():



	mainwin.connect("destroy", Gtk.main_quit)

	pygame.display.init()
	GLib.threads_init()
	Gdk.threads_init()
	Gdk.threads_enter()
	thread1.start()
	thread2.start()
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

		joystickid

		pygame.event.pump()


	#main code
		if joystickinuse.get_id() == joystickid:
			


			None


			

		elif joystickid != -1:
			
			joystickinuse = pygame.joystick.Joystick(joystickid)
			mainwin.scrolled_term.insert_text_term('Connected: ' + joystickinuse.get_name())
			contbox.butbox.joystick = joystickinuse



		if mainwin.appmenu.controllerwin.get_visible():

			if joystickid != -1:
				
				buttonlist = contbox.butbox.buttonlist
				axeslist = contbox.butbox.axeslist
				hatlist = contbox.butbox.hatlist



	
				
				for i, button in enumerate(buttonlist[joystickinuse.get_id()]):


					value = int(joystickinuse.get_button(i))
					button.levelbar.set_value((value * 95) + 4)
		
				for i, axis in enumerate(axeslist[joystickinuse.get_id()]):
					value = joystickinuse.get_axis(i)

					value = 50 + value * 45	
					axis.levelbar.set_value(value)
				

				for i in range(joystickinuse.get_numhats()):
					value = joystickinuse.get_hat(i)	#get hat i: joystick inuse

					valuex = 50 + value[0] * 45


					valuey = 50 + value[1] * 45

					hatlist[joystickinuse.get_id()][i].levelbar.set_value(valuex)
					hatlist[joystickinuse.get_id()][i+1].levelbar.set_value(valuey)



					


def serialbg():
	port = mainwin.serialportbox.useport
	while(True):
		while(port.is_open):
			print('hi')






thread1 = threading.Thread(target=background)
thread1.daemon = True

thread2 = threading.Thread(target=serialbg)
thread2.daemon = True



app_main()





