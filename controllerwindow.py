import gi
import pygame
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk



class ControllerWindow(Gtk.Window):
	def __init__(self):

		Gtk.Window.__init__(self, title="Settings")
		self.set_default_size(600,600)

		mainbox = Gtk.Box(orientation = 'horizontal', spacing = 10)
		serialbox = Gtk.Box(orientation = 'vertical', spacing = 10)


		
		sep = Gtk.VSeparator()
		self.controllerbox = ControllerBox()

		self.controllerbox.endpointbutbox.entrymin.connect("activate", self.entrymin_func)

	
		mainbox.add(self.controllerbox)

		self.add(mainbox)

	def entrymin_func(self, widget):
		self.grab_focus()
		
		return True

class ControllerBox(Gtk.Box):

	def __init__(self):
		Gtk.Box.__init__(self, orientation = 'vertical')
		

		self.joysticks = None

		contbox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		contbox.set_margin_bottom(20)
		contbox.set_size_request(750,0)
		self.butbox = ButtonBox()
		self.butbox.set_size_request(520,400)
		contlabel = Gtk.Label("Controller: ")

		self.scrollbuttonwindow = Gtk.ScrolledWindow()
		self.scrollbuttonwindow.set_min_content_height(500)
	#	self.scrollbuttonwindow.set_size_request(550,550)
		self.scrollbuttonwindow.set_propagate_natural_width(True)
		self.scrollbuttonwindow.set_propagate_natural_height(True)
		self.scrollbuttonwindow.set_overlay_scrolling(True)


		labelbox = Gtk.Box(orientation = 'horizontal')
		buttonlabel = Gtk.Label("BUTTONS:")
	#	buttonlabel.set_halign(Gtk.Align.START)
		buttonlabel.set_markup("<b>BUTTONS:</b>")
		buttonlabel.set_width_chars(20)
		buttonlabel.set_margin_left(150)

		axeslabel = Gtk.Label("AXIS:")
	#	axeslabel.set_halign(Gtk.Align.START)
		axeslabel.set_markup("<b>AXIS:</b>")
		axeslabel.set_width_chars(20)
		axeslabel.set_margin_right(0)
	
		hatlabel = Gtk.Label("HATS: ")
	#	hatlabel.set_halign(Gtk.Align.START)
		hatlabel.set_markup("<b>HAT:</b>")
		hatlabel.set_width_chars(20)
		hatlabel.set_margin_right(0)
		


		self.endpointbutbox = EndPointBox(label = 'Button:')
		endpointhatbox = EndPointBox(label = 'Hat: ')
		endpointaxisbox = EndPointBox(label = 'Axis:')		



		sep = Gtk.Separator()
		sep2 = Gtk.Separator()



		self.contcombo = Gtk.ComboBoxText()
		self.contcombo.set_size_request(500,10)


		self.rightbox = Gtk.Box(orientation = 'vertical')
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




		self.rightbox.add(self.endpointbutbox)
		self.rightbox.add(endpointhatbox)
		self.rightbox.add(endpointaxisbox)

		
		self.scrollbuttonwindow.add(self.butbox)
		

		secbox.add(self.rightbox)
		secbox.add(sep2)
		secbox.add(self.scrollbuttonwindow)
		secbox.add(sep)
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

		self.buttonattr = []
		self.hatattr = []
		self.axesattr = []



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
		self.set_margin_bottom(5)
		self.set_margin_top(5)
		self.set_margin_right(10)
	#	self.set_margin_left(10)
		
		

		self.levelbar = Gtk.LevelBar()
		self.levelbar.set_min_value(0)
		self.levelbar.set_max_value(100)
		self.levelbar.set_value(5)
		self.levelbar.set_margin_top(5)

		self.levelbar.set_margin_right(5)
		self.levelbar.set_margin_left(5)



		self.label = Gtk.Label()
		self.label.set_label(levlabel)
		

		self.add(self.label)
		self.add(self.levelbar)



class EndPointBox(Gtk.Box):

	def __init__(self, label):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 5)
		self.set_margin_right(10)
		self.set_margin_left(10)
		inputbox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		minbox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		maxbox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		sep = Gtk.Separator()

		inputlabel = Gtk.Label(label)
		inputlabel.set_markup("<b>" + label + "</b>")
		inputlabel.set_halign(Gtk.Align.START)
		inputlabel.set_margin_left(0)
		inputcombo = Gtk.ComboBoxText()
	#	inputcombo.set_margin_left(35)
		inputcombo.set_size_request(75,0)
		inputinv = Gtk.ToggleButton(label = "Inv")

	#	inputbox.add(inputlabel)
		inputbox.add(inputcombo)
		inputbox.add(inputinv)


		labelmin = Gtk.Label('Min:')
		labelmin.set_halign(Gtk.Align.START)
		labelmin.set_margin_left(0)

		labelmax = Gtk.Label('Max:')
		labelmax.set_halign(Gtk.Align.START)
		labelmax.set_margin_left(0)

		self.entrymin = Gtk.Entry()
		self.entrymin.set_width_chars(5)
		self.entrymax = Gtk.Entry()
		self.entrymax.set_width_chars(5)
	#	minbox.add(labelmin)
		minbox.add(self.entrymin)
	#	maxbox.add(labelmax)
		maxbox.add(self.entrymax)

		sep.set_margin_top(25)
	#	sep.set_margin_bottom(25)

		self.entrymin.set_activates_default(True)
		self.entrymax.set_activates_default(True)
	#	self.entrymin.connect("activate", self.entrymin_func)



		self.add(inputlabel)
		self.add(inputbox)
		self.add(labelmin)	
		self.add(minbox)	
		self.add(labelmax)	
		self.add(maxbox)	
		self.add(sep)

	

	def entrymin_func(self, widget):
		self.grab_focus()

















