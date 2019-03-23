import gi
import serial
import serial.tools.list_ports
import time


import serialwindow
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk



#Gtk window subclass : main window
class MainWindow(Gtk.Window):

	

	def __init__(self):
		Gtk.Window.__init__(self, title="Serial Term")
		self.set_default_size(800, 600)
		box = Gtk.Box(orientation = 'horizontal')

		


	#	sidestack.set_size_request(200,600)

		stack = Gtk.Stack()

		

		
		label = Gtk.Label("testq32o2o34u")
		
		label2 = Gtk.Label(label = "yoo world")
	
					
		stack.add_titled(label, "entry", "test1")
		stack.add_titled(label2, 'hello', 'test1')


		sidestack = Gtk.StackSidebar()
		sidestack.set_stack(stack)

		box.add(sidestack)
		box.add(stack)

		self.add(box)	

		self.show_all()

mainwin = MainWindow()
mainwin.connect("destroy", Gtk.main_quit)
mainwin.show_all()
Gtk.main()

