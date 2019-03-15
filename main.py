import window
import threading
import time
import serial
import pygame
import sys

from gi.repository import Gtk, Gdk, GLib



mainwin = window.MainWindow()

mainwin.connect("destroy", Gtk.main_quit)
pygame.display.init()

joystickid = mainwin.appmenu.serialwin.controllerbox.contcombo.get_active()
tbuf = mainwin.scrolled_term.term_text.get_buffer()

def background():
	pygame.joystick.init()
	#joysticklist = mainwin.appmenu.serialwin.controllerbox.joysticks
	joystickid = mainwin.appmenu.serialwin.controllerbox.contcombo.get_active()

	while(joystickid is -1):
		joystickid = mainwin.appmenu.serialwin.controllerbox.contcombo.get_active()


	joystickinuse = pygame.joystick.Joystick(joystickid)
	joystickinuse.init()
	
	#Window Terminal
	tbuf.insert_at_cursor('Connected:' + joystickinuse.get_name() + '\n')
	mainwin.scrolled_term.term_text.set_buffer(tbuf)	

	while(True):
		joystickid = mainwin.appmenu.serialwin.controllerbox.contcombo.get_active()

		if joystickinuse.get_id() == joystickid:
			pygame.event.pump()
	
			#print(joystickinuse.get_axis(1))
			returnval = joystickinuse.get_axis(1)
			mainwin.level1.set_value(int(returnval*100))

			
	
			print(joystickid)
			print(joystickinuse.get_id())		



		elif joystickid != -1:
			
			joystickinuse.quit
			joystickinuse = None
			joystickinuse = pygame.joystick.Joystick(joystickid)
			joystickinuse.init()
			tbuf.insert_at_cursor('open' + '\n')
			mainwin.scrolled_term.term_text.set_buffer(tbuf)	

		







#mainwin.appmenu.serialwin

thread1 = threading.Thread(target=background)
thread1.daemon = True






GLib.threads_init()
Gdk.threads_init()
Gdk.threads_enter()
thread1.start()
window.Gtk.main()
#pygame.quit()
Gdk.threads_leave();
