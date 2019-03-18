import window
import threading
import time
import serial
import pygame
import sys
from multiprocessing import Process, Manager
from gi.repository import Gtk, Gdk, GLib

mainwin = window.MainWindow()
joystickid = mainwin.appmenu.serialwin.controllerbox.contcombo.get_active()


def app_main():

	mainwin.connect("destroy", Gtk.main_quit)
	pygame.display.init()
	GLib.threads_init()
	Gdk.threads_init()
	Gdk.threads_enter()
	thread1.start()
	
	window.Gtk.main()
	#pygame.quit()
	Gdk.threads_leave();



def background():
	pygame.joystick.init()
	tbuf = mainwin.scrolled_term.term_text.get_buffer()
	contbox = mainwin.appmenu.serialwin.controllerbox
	joysticklist = mainwin.appmenu.serialwin.controllerbox.joysticks
	joystickid = mainwin.appmenu.serialwin.controllerbox.contcombo.get_active()

	while(joystickid is -1):
		joystickid = mainwin.appmenu.serialwin.controllerbox.contcombo.get_active()


	joystickinuse = pygame.joystick.Joystick(joystickid)
	joystickinuse.init()

	#Window Terminal
	tbuf.insert_at_cursor('Connected: ' + joystickinuse.get_name() + '\n')
	mainwin.scrolled_term.term_text.set_buffer(tbuf)
	contbox.butbox.joystick = joystickinuse

	while(True):
		joystickid = mainwin.appmenu.serialwin.controllerbox.contcombo.get_active()
		
		pygame.event.pump()

	#pygame.event.set_blocked(None)
		pygame.event.set_blocked(pygame.JOYAXISMOTION)
	#main code
		if joystickinuse.get_id() == joystickid:
			
			
			#print(joystickinuse.get_axis(1))
			returnval = joystickinuse.get_axis(1)
			mainwin.level1.set_value(int(returnval*100)+2)
			
		#	mainwin.appmenu.serialwin.controllerbox.butbox.buttonlist[2][0].set_value = 1
		#	print(joystickinuse.get_hat(0))



		elif joystickid != -1:
			
			joystickinuse = pygame.joystick.Joystick(joystickid)
			joystickinuse.init()

			tbuf.insert_at_cursor('Connected: ' + joystickinuse.get_name() + '\n')
			mainwin.scrolled_term.term_text.set_buffer(tbuf)
			contbox.butbox.joystick = joystickinuse
			time.sleep(1)


		if mainwin.appmenu.serialwin.get_visible():

			buttonlist = contbox.butbox.buttonlist

			for i, button in enumerate(buttonlist[joystickinuse.get_id()]):
				value = int(joystickinuse.get_button(i))
				button.levelbar.set_value((value + 1)*5)
				#print(int(joystickinuse.get_button(i)))
	
			




thread1 = threading.Thread(target=background)
thread1.daemon = True



app_main()





