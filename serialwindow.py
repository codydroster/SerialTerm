import gi
import pygame
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk



class SerialWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Settings")
		self.set_default_size(600,600)
		mainbox = Gtk.Box(orientation = 'horizontal', spacing = 10)

		serialbox = Gtk.Box(orientation = 'vertical', spacing = 10)
		sep = Gtk.VSeparator()
		self.controllerbox = ControllerBox()






		conbutton = Gtk.Button(label = "connect")


		self.row1 = SerialWindowBox()
		self.row1.label.set_text("Baudrate:")	
		self.row1.combo.append('0', '9600')
		self.row1.combo.append('1', "19200")
		self.row1.combo.append('2', "115200")
		self.row1.combo.set_active_id('0')
		serialbox.add(self.row1)

		self.row2 = SerialWindowBox()	
		self.row2.label.set_text("Data Bits:")
		self.row2.combo.append('0', '5')
		self.row2.combo.append('1', '6')
		self.row2.combo.append('2', '7')
		self.row2.combo.append('3', '8')
		self.row2.combo.set_active_id('3')
		serialbox.add(self.row2)

		self.row3 = SerialWindowBox()
		self.row3.label.set_text("Parity:     ")
		self.row3.combo.append('0', 'None')
		self.row3.combo.append('1', 'Odd')
		self.row3.combo.append('2', 'Even')
		self.row3.combo.set_active_id('0')
		serialbox.add(self.row3)

		self.row4 = SerialWindowBox()
		self.row4.label.set_text("Stop Bits:")
		self.row4.combo.append('0', '1')
		self.row4.combo.append('1', '1.5')
		self.row4.combo.append('2', '2')
		self.row4.combo.set_active_id('0')
		serialbox.add(self.row4)


		mainbox.add(serialbox)
		mainbox.add(sep)
		mainbox.add(self.controllerbox)

		self.add(mainbox)

		

class ControllerBox(Gtk.Box):

	def __init__(self):
		Gtk.Box.__init__(self, orientation = 'vertical')
		pygame.joystick.init()		

		self.joysticks = None

		contbox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		contbox.set_margin_bottom(20)
		self.butbox = ButtonBox()
		contlabel = Gtk.Label("Controller: ")
		self.contcombo = Gtk.ComboBoxText()
		self.contcombo.set_size_request(500,10)


		self.rightbox = Gtk.Box()
		secbox = Gtk.Box(orientation = 'horizontal')
		self.scanbut = Gtk.Button(label = "scan")
		self.scanbut.set_margin_right(5)	


		
		self.scanbut.connect("clicked", self.scan_cont)
		self.contcombo.connect("changed", self.map)
		contbox.add(contlabel)
		contbox.add(self.contcombo)
		contbox.add(self.scanbut)


		self.add(contbox)
		secbox.add(self.butbox)
		secbox.add(self.rightbox)
		self.add(secbox)

	def scan_cont(self, widget):
		
		self.contcombo.remove_all()
		pygame.joystick.init()
		self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

		for j, joy in enumerate(self.joysticks):
			self.contcombo.insert_text(j, joy.get_name())
		
		self.butbox.updatebut()


	def map(self, widget):
		self.butbox.joystickid = self.contcombo.get_active()

		self.butbox.map2()
		

class SerialWindowBox(Gtk.Box):
	
	def __init__(self):	
		Gtk.Box.__init__(self, orientation='horizontal', spacing=10)
		self.combo = Gtk.ComboBoxText()

		self.label = Gtk.Label()
		self.add(self.label)
		self.label.set_width_chars(10)
		self.label.xpad = 2
	

		self.add(self.combo)
	



class ButtonBox(Gtk.Box):
	
	def __init__(self):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 5)

		self.activebox = Gtk.Box(orientation = 'vertical', spacing = 5)
		self.joystickid = None
		buttonlabel = Gtk.Label("Buttons: ")
		self.activebox2 = []

		self.joysticks = None

		self.buttonlist = []

		self.numbuttons = 0

		self.add(buttonlabel)
		self.button = Gtk.Label("test")


	def updatebut(self):
		

		self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

		for j, joy in enumerate(self.joysticks):
			joy.init()
			self.buttonlist.append([])
			self.activebox2.insert(j, Gtk.Box(orientation = 'vertical'))
			for i in range(joy.get_numbuttons()):
				self.buttonlist[j].insert(i, ButtonLevel(levlabel=str(i) + ':'))

				self.activebox2[j].add(self.buttonlist[j][i])
	

	

	def map2(self):

		self.show_all()
		
		for box in self.activebox2:
			if box in self.get_children():
				self.remove(box)

		for i in range(pygame.joystick.get_count()):
			
			if self.joystickid == i:
				self.add(self.activebox2[i])
				self.show_all()
				


class ButtonLevel(Gtk.Box):
	
	def __init__(self, levlabel):
		Gtk.Box.__init__(self, orientation = 'vertical')

		
		self.levelbar = Gtk.LevelBar()
		self.levelbar.set_min_value(0)
		self.levelbar.set_max_value(10)
		self.levelbar.set_value(30)	


		self.label = Gtk.Label()
		self.label.set_label(levlabel)
		
		
		self.add(self.label)
		self.add(self.levelbar)
		






