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
		

		self.joysticks = None

		contbox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		contbox.set_margin_bottom(20)
		self.butbox = ButtonBox()
		contlabel = Gtk.Label("Controller: ")

		labelbox = Gtk.Box(orientation = 'horizontal')
		buttonlabel = Gtk.Label("BUTTONS:")
		buttonlabel.set_margin_right(103)
		
		sep = Gtk.Separator()

		axeslabel = Gtk.Label("AXES:")
		axeslabel.set_margin_right(110)
	
		hatlabel = Gtk.Label("HATS: ")
		hatlabel.set_margin_right(118)

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
		labelbox.add(buttonlabel)
		labelbox.add(hatlabel)
		labelbox.add(axeslabel)

		self.add(labelbox)
		self.add(sep)
		secbox.add(self.butbox)
		secbox.add(self.rightbox)
		self.add(secbox)

	def scan_cont(self, widget):
		
		self.contcombo.remove_all()

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
		Gtk.Box.__init__(self, orientation = 'horizontal', spacing = 5)

		
		self.joystickid = None
		buttonlabel = Gtk.Label("Buttons: ")
		

		self.buttonbox = []
		self.hatbox = []
		self.axesbox = []

		self.buttonlist = []
		self.hatlist = []
		self.axeslist = []

		self.joysticks = None




	def updatebut(self):
		
		self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

		self.buttonlist = []
		self.hatlist = []
		self.axeslist = []


		for j, joy in enumerate(self.joysticks):
			
			if not joy.get_init():
				joy.init()

		
		#buttonlist
			self.buttonlist.append([])
			self.buttonbox.insert(j, Gtk.Box(orientation = 'vertical'))
			for i in range(joy.get_numbuttons()):
				self.buttonlist[j].insert(i, ButtonLevel(levlabel=str(i) + ':'))
				self.buttonlist[j][i].label.set_margin_right(140)
				self.buttonbox[j].add(self.buttonlist[j][i])
	
		#axislist
			self.axeslist.append([])
			self.axesbox.insert(j, Gtk.Box(orientation = 'vertical'))
			for i in range(joy.get_numaxes()):
				self.axeslist[j].insert(i, ButtonLevel(levlabel=str(i) + ':'))
				self.axeslist[j][i].label.set_margin_right(130)
				self.axesbox[j].add(self.axeslist[j][i])
	
		#hatlist
			self.hatlist.append([])
			self.hatbox.insert(j, Gtk.Box(orientation = 'vertical'))
			for i in range(joy.get_numhats()+1):
				self.hatlist[j].insert(i, ButtonLevel(levlabel=str(i) + ':'))
				self.hatlist[j][i].label.set_margin_right(130)
				self.hatbox[j].add(self.hatlist[j][i])



	def map2(self):

		self.show_all()
		
	#buttonlist
		for box in self.buttonbox:
			if box in self.get_children():
				self.remove(box)

		for i in range(pygame.joystick.get_count()):
			
			if self.joystickid == i:
				self.add(self.buttonbox[i])
				self.show_all()

	
	#hatlist
		for box in self.hatbox:
			if box in self.get_children():
				self.remove(box)

		for i in range(pygame.joystick.get_count()):
			
			if self.joystickid == i:
				self.add(self.hatbox[i])
				self.show_all()

#axeslist
		for box in self.axesbox:
			if box in self.get_children():
				self.remove(box)

		for i in range(pygame.joystick.get_count()):
			
			if self.joystickid == i:
				self.add(self.axesbox[i])
				self.show_all()




class ButtonLevel(Gtk.Box):
	
	def __init__(self, levlabel):
		Gtk.Box.__init__(self, orientation = 'vertical')
		self.set_size_request(150,0)
		self.set_margin_bottom(10)
		
		self.levelbar = Gtk.LevelBar()
		self.levelbar.set_min_value(0)
		self.levelbar.set_max_value(100)
		self.levelbar.set_value(5)	


		self.label = Gtk.Label()


		self.label.set_label(levlabel)
		
		
		self.add(self.label)
		self.add(self.levelbar)
		






