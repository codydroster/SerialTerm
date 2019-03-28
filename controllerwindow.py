import gi
import pygame
import bytetype
import structs
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject



class ControllerWindow(Gtk.Window):
	def __init__(self):

		Gtk.Window.__init__(self, title="Settings")
		self.set_default_size(1100,650)

		mainbox = Gtk.Box(orientation = 'horizontal', spacing = 10)
		serialbox = Gtk.Box(orientation = 'vertical', spacing = 10)



		sep = Gtk.VSeparator()
		self.controllerbox = ControllerBox()


		self.controllerbox.bytebox.typeadd.connect('clicked', self.map_connect)
		self.controllerbox.endpointbutbox.entrymax.connect("activate", self.lose_focus)
		self.controllerbox.endpointhatbox.entrymax.connect("activate", self.lose_focus)
		self.controllerbox.endpointaxisbox.entrymax.connect("activate", self.lose_focus)


		mainbox.add(self.controllerbox)
		self.add(mainbox)

	def lose_focus(self, widget):

		self.set_focus(None)
		return True
		

	#connect bytebox entries to lose focus on event: ENTER
	def map_connect(self, widget):
		for ele in self.controllerbox.bytebox.entryarray:
			if hasattr(ele, 'byteentry'):
				ele.byteentry.connect("activate", self.lose_focus)

	

class ControllerBox(Gtk.Box):

	def __init__(self):
		Gtk.Box.__init__(self, orientation = 'vertical')
		

		self.joysticks = None

		contbox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		contbox.set_margin_bottom(20)
		contbox.set_margin_left(10)
		contbox.set_size_request(750,0)
		self.butbox = ButtonBox()
		self.labelbox = Gtk.Box(orientation = 'horizontal')
		self.butbox.set_size_request(520,400)
		contlabel = Gtk.Label("Controller: ")


	#component window
		self.scrollbuttonwindow = Gtk.ScrolledWindow()
		self.scrollbuttonwindow.set_min_content_height(500)
		self.scrollbuttonwindow.set_propagate_natural_width(True)
		self.scrollbuttonwindow.set_propagate_natural_height(True)
		self.scrollbuttonwindow.set_overlay_scrolling(True)


	#component labels
		buttonlabel = Gtk.Label("BUTTONS:")
		buttonlabel.set_markup("<b>BUTTONS:</b>")
		buttonlabel.set_width_chars(20)
		buttonlabel.set_margin_left(150)
		buttonlabel.set_margin_right(8)

		axislabel = Gtk.Label("AXIS:")
		axislabel.set_markup("<b>AXIS:</b>")
		axislabel.set_width_chars(20)
		axislabel.set_margin_right(8)
	
		hatlabel = Gtk.Label("HATS: ")
		hatlabel.set_markup("<b>HAT:</b>")
		hatlabel.set_width_chars(20)
		hatlabel.set_margin_right(8)
		

	#EndPointBox
		self.endpointbutbox = EndPointBox(label='Button:', typ='button')

		self.endpointhatbox = EndPointBox(label='Hat: ', typ='hat')
		self.endpointaxisbox = EndPointBox(label='Axis:',typ='axis')		


		self.endpointbutbox.entrymax.connect('focus-out-event', self.update_endpoints)
		self.endpointaxisbox.entrymax.connect('focus-out-event', self.update_endpoints)
		self.endpointhatbox.entrymax.connect('focus-out-event', self.update_endpoints)


		self.endpointbutbox.inputcombo.connect('changed', self.input_changed)
		self.endpointaxisbox.inputcombo.connect('changed', self.input_changed)
		self.endpointhatbox.inputcombo.connect('changed', self.input_changed)
		
		self.endpointaxisbox.inputinv.connect('toggled', self.invert)
		self.endpointhatbox.inputinv.connect('toggled', self.invert)



		sep = Gtk.Separator()
		sep2 = Gtk.Separator()
		secbox = Gtk.Box(orientation = 'horizontal')


		self.contcombo = Gtk.ComboBoxText()
		self.contcombo.set_size_request(500,10)


		self.leftbox = Gtk.Box(orientation = 'vertical')
	#bytebox
		self.bytebox = ByteBox()
		self.scanbut = Gtk.Button(label = "scan")
		self.scanbut.set_margin_right(5)	


		
		self.scanbut.connect("clicked", self.scan_cont)
		self.contcombo.connect("changed", self.map)
		

		contbox.add(contlabel)
		contbox.add(self.contcombo)
		contbox.add(self.scanbut)
		self.add(contbox)
	

		self.labelbox.add(buttonlabel)
		self.labelbox.add(hatlabel)
		self.labelbox.add(axislabel)
		self.add(self.labelbox)




		self.leftbox.add(self.endpointbutbox)
		self.leftbox.add(self.endpointhatbox)
		self.leftbox.add(self.endpointaxisbox)
		
		self.scrollbuttonwindow.add(self.butbox)
		

		secbox.add(self.leftbox)
		secbox.add(sep2)
		secbox.add(self.scrollbuttonwindow)
		secbox.add(sep)
		secbox.add(self.bytebox)
		self.add(secbox)


	def scan_cont(self, widget):
		
		self.contcombo.remove_all()

		self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

		for j, joy in enumerate(self.joysticks):
			self.contcombo.insert_text(j, joy.get_name())
		
		
		self.butbox.updatebut()

	def update_endpoints(self, widget, event):
		endbut = self.endpointbutbox
		endaxis = self.endpointaxisbox
		endhat = self.endpointhatbox

		if widget is endbut.entrymax:
			self.butbox.buttonattr[self.contcombo.get_active()][endbut.inputcombo.get_active()].max = float(endbut.entrymax.get_text())

		elif widget is endaxis.entrymax:
			self.butbox.axisattr[self.contcombo.get_active()][endaxis.inputcombo.get_active()].max = float(endaxis.entrymax.get_text())
	
		elif widget is endhat.entrymax:
			self.butbox.hatattr[self.contcombo.get_active()][endhat.inputcombo.get_active()].max = float(endhat.entrymax.get_text())

		

	def input_changed(self, widget):
		endbut = self.endpointbutbox
		endaxis = self.endpointaxisbox
		endhat = self.endpointhatbox

		#button
		if widget is endbut.inputcombo:
			endbut.entrymax.set_text(str(self.butbox.buttonattr[self.contcombo.get_active()][endbut.inputcombo.get_active()].max))

		#axis
		if widget is endaxis.inputcombo:
			endaxis.entrymax.set_text(str(self.butbox.axisattr[self.contcombo.get_active()][endaxis.inputcombo.get_active()].max))
			
			if self.butbox.axisattr[self.contcombo.get_active()][endaxis.inputcombo.get_active()].inverted == 1:
				endaxis.inputinv.set_active(False)
			else:
				endaxis.inputinv.set_active(True)


		#hat
		if widget is endhat.inputcombo:
			endhat.entrymax.set_text(str(self.butbox.hatattr[self.contcombo.get_active()][endhat.inputcombo.get_active()].max))

			if self.butbox.hatattr[self.contcombo.get_active()][endhat.inputcombo.get_active()].inverted == 1:
				endhat.inputinv.set_active(False)
			else:
				endhat.inputinv.set_active(True)


	
	def invert(self, widget):
		endaxis = self.endpointaxisbox
		endhat = self.endpointhatbox

		if widget is endaxis.inputinv:
			if endaxis.inputinv.get_active() == True:
				self.butbox.axisattr[self.contcombo.get_active()][endaxis.inputcombo.get_active()].inverted = -1
			else:
				self.butbox.axisattr[self.contcombo.get_active()][endaxis.inputcombo.get_active()].inverted = 1

		elif widget is endhat.inputinv:
			if endhat.inputinv.get_active() == True:
				self.butbox.hatattr[self.contcombo.get_active()][endhat.inputcombo.get_active()].inverted = -1
			else:
				self.butbox.hatattr[self.contcombo.get_active()][endhat.inputcombo.get_active()].inverted = 1


			
#controller input changed
	def map(self, widget):
		self.butbox.joystickid = self.contcombo.get_active()
		self.bytebox.joystickid = self.contcombo.get_active()
		self.butbox.map2()

		self.endpointbutbox.attr = self.butbox.buttonattr
		self.endpointaxisbox.attr = self.butbox.axisattr
		self.endpointhatbox.attr = self.butbox.hatattr
		
		self.endpointbutbox.joystickid = self.contcombo.get_active()
		self.endpointaxisbox.joystickid = self.contcombo.get_active()
		self.endpointhatbox.joystickid = self.contcombo.get_active()

		self.endpointbutbox.map()
		self.endpointaxisbox.map()
		self.endpointhatbox.map()

		self.bytebox.map_axis()
		self.bytebox.map_button()
		self.bytebox.map_hat()

	#	self.show_all()

class ButtonBox(Gtk.Box):
	
	def __init__(self):
		Gtk.Box.__init__(self, orientation = 'horizontal', spacing = 5)

		
		self.joystickid = None
		buttonlabel = Gtk.Label("Buttons: ")
		

		self.buttonbox = []
		self.hatbox = []
		self.axisbox = []

		self.buttonlist = []
		self.hatlist = []
		self.axislist = []

		self.joysticks = None

		self.buttonattr = []
		self.hatattr = []
		self.axisattr = []



	def updatebut(self):
		
		self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

		self.buttonattr = []	#level objects for controller window
		self.hatattr = []
		self.axisattr = []


		for j, joy in enumerate(self.joysticks):
			
			if not joy.get_init():
				joy.init()

		
		#buttonlist
			self.buttonlist.append([])
			self.buttonattr.append([])

			self.buttonbox.insert(j, Gtk.Box(orientation = 'vertical'))
			for i in range(joy.get_numbuttons()):
				self.buttonattr[j].insert(i, structs.ButtonAttributes(name = str(i)))
				self.buttonbox[j].add(self.buttonattr[j][i].box)


	
		#axislist
			self.axislist.append([])
			self.axisattr.append([])

			self.axisbox.insert(j, Gtk.Box(orientation = 'vertical'))
			for i in range(joy.get_numaxes()):
				self.axisattr[j].insert(i, structs.AxisAttributes(name = str(i)))	
				self.axisbox[j].add(self.axisattr[j][i].box)


	
		#hatlist
			self.hatlist.append([])
			self.hatattr.append([])

			self.hatbox.insert(j, Gtk.Box(orientation = 'vertical'))
			for i in range(joy.get_numhats()+1):
				self.hatattr[j].insert(i, structs.HatAttributes(name = str(i)))
				self.hatbox[j].add(self.hatattr[j][i].box)




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

	#axislist
		for box in self.axisbox:
			if box in self.get_children():
				self.remove(box)

		for i in range(pygame.joystick.get_count()):
			
			if self.joystickid == i:
				self.add(self.axisbox[i])
				self.show_all()



class EndPointBox(Gtk.Box):

	def __init__(self, label, typ):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 5)
		self.set_margin_right(10)
		self.set_margin_left(10)

		inputbox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		self.minbox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		self.maxbox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		sep = Gtk.Separator()

		inputlabel = Gtk.Label(label)
		inputlabel.set_markup("<b>" + label + "</b>")
		inputlabel.set_halign(Gtk.Align.START)
		inputlabel.set_margin_left(0)

		self.attr = None
		self.joystickid = None



		self.inputcombo = Gtk.ComboBoxText()
		self.inputcombo.set_size_request(75,0)
		inputbox.add(self.inputcombo)
		

		if typ != 'button':
			self.inputinv = Gtk.ToggleButton(label = "Inv")
			inputbox.add(self.inputinv)


		labelmax = Gtk.Label('Displacement:')
		labelmax.set_halign(Gtk.Align.START)
		labelmax.set_margin_left(0)

		self.entrymax = Gtk.Entry()
		self.entrymax.set_width_chars(10)


		self.maxbox.add(self.entrymax)

		sep.set_margin_top(20)
		sep.set_margin_bottom(5)


		self.add(inputlabel)
		self.add(inputbox)
	
		self.add(labelmax)	
		self.add(self.maxbox)	
		self.add(sep)


	def map(self):
		
		self.inputcombo.remove_all()

		for i, comp in enumerate(self.attr[self.joystickid]):
			self.inputcombo.insert_text(i, comp.name)

		self.inputcombo.set_active(0)

	






class ByteBox(Gtk.Box):

	def __init__(self):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 5)
		self.headerbox = Gtk.Box(orientation = 'horizontal', spacing =5)
		self.headerbox.set_margin_right(5)
		self.headerbox.set_margin_left(5)
		self.headerbox.set_margin_bottom(15)
		self.typelabel = Gtk.Label("TYPE: ")
		self.typebox = Gtk.ComboBoxText()
		self.typebox.set_size_request(275,0)
		
		self.typeadd = Gtk.Button(label = 'ADD')

		self.typeadd.connect('clicked', self.add_byte)
		self.entryarray = []

		self.transmitbytes = [0x42, 0x43, (0x3e8 >> 8), (0x3e8 & 0xff)]

	#current joystick
		self.joystickid = None
		
	#byte types
		self.typebox.insert_text(0, "Constant Value: 8 Bit")
		self.typebox.insert_text(1, "Constant + Axis + Button: 8 Bit")
		self.typebox.insert_text(2, "Constant + Axis + Button: 16 Bit")
		self.typebox.insert_text(3, "Constant + Axis + Hat: 8 Bit")
		self.typebox.insert_text(4, "Constant + Axis + Hat: 16 Bit")
		self.typebox.set_active(0)


		self.headerbox.add(self.typelabel)
		self.headerbox.add(self.typebox)
		self.headerbox.add(self.typeadd)
		self.add(self.headerbox)



	def map_axis(self):
		for val in self.entryarray:
			if hasattr(val, 'axiscombo'):
				val.axiscombo.remove_all()

				if self.joystickid != -1:
					if self.joystickid != None:

						for i in range(pygame.joystick.Joystick(self.joystickid).get_numaxes()):
							val.axiscombo.insert_text(i, str(i))
						val.axiscombo.insert_text(-1, ' ')



	def map_button(self):
		for val in self.entryarray:
			if hasattr(val, 'buttonlab'):
				val.buttoncombo0.remove_all()
				val.buttoncombo1.remove_all()
				if self.joystickid != -1:
					if self.joystickid != None:

						for i in range(pygame.joystick.Joystick(self.joystickid).get_numbuttons()):
							val.buttoncombo0.insert_text(i, str(i))
							val.buttoncombo1.insert_text(i, str(i))
						val.buttoncombo0.insert_text(-1, ' ')
						val.buttoncombo1.insert_text(-1, ' ')



	def map_hat(self):
		for val in self.entryarray:
			if hasattr(val, 'hatlabel'):
				val.hatcombo.remove_all()

				if self.joystickid != -1:
					if self.joystickid != None:

						for i in range(pygame.joystick.Joystick(self.joystickid).get_numhats()+1):
							val.hatcombo.insert_text(i, str(i))
						val.hatcombo.insert_text(-1, ' ')



	def add_byte(self, widget):
		byteindex = 0
		for byte in self.entryarray:
			byteindex += byte.numbytes
			

		if self.typebox.get_active() == 0:
			
			self.entryarray.append(bytetype.ConstantValue(byteindex))
			currentbyte = self.entryarray[len(self.entryarray)-1]

			self.add(currentbyte)
			
			currentbyte.byteentry.connect('focus-out-event', self.update_entry)
	
			

		if self.typebox.get_active() == 1:
			self.entryarray.append(bytetype.ConstantAxis(byteindex))
			currentbyte = self.entryarray[len(self.entryarray) - 1]
			
			currentbyte.byteentry.connect('focus-out-event', self.update_entry)
			currentbyte.axiscombo.connect('changed', self.update)
			currentbyte.buttoncombo0.connect('changed', self.update)
			currentbyte.buttoncombo1.connect('changed', self.update)
	
			self.add(currentbyte)
			

		if self.typebox.get_active() == 2:

			self.entryarray.append(bytetype.ConstantAxis2B(byteindex))
			currentbyte = self.entryarray[len(self.entryarray)-1]

			currentbyte.byteentry.connect('focus-out-event', self.update_entry)
			currentbyte.axiscombo.connect('changed', self.update)
			currentbyte.buttoncombo0.connect('changed', self.update)
			currentbyte.buttoncombo1.connect('changed', self.update)

			self.add(currentbyte)
			


		if self.typebox.get_active() == 3:

			self.entryarray.append(bytetype.ConstantAxisHat(byteindex))
			currentbyte = self.entryarray[len(self.entryarray)-1]

			currentbyte.byteentry.connect('focus-out-event', self.update_entry)
			currentbyte.axiscombo.connect('changed', self.update)
			currentbyte.hatcombo.connect('changed', self.update)

			self.add(currentbyte)
		



		if self.typebox.get_active() == 4:

			self.entryarray.append(bytetype.ConstantAxisHat2B(byteindex))
			currentbyte = self.entryarray[len(self.entryarray)-1]

			currentbyte.byteentry.connect('focus-out-event', self.update_entry)
			currentbyte.axiscombo.connect('changed', self.update)
			currentbyte.hatcombo.connect('changed', self.update)

			self.add(currentbyte)
			

		self.map_axis()
		self.map_button()
		self.map_hat()



	def update_entry(self, widget, event):
		for byte in self.entryarray:
			if widget is byte.byteentry:
				try:
					byte.byteval = int(byte.byteentry.get_text(), 0)
					print(byte.byteval)
				except:
					byte.byteval = 0




	def update(self, widget):
		for byte in self.entryarray:
			if hasattr(byte, 'axiscombo'):
				if widget is byte.axiscombo:
					if byte.axiscombo.get_active_text() == ' ':
						byte.axis = None
					else:				
						byte.axis = byte.axiscombo.get_active()


		for byte in self.entryarray:
			if hasattr(byte, 'button0'):
				if widget is byte.buttoncombo0:
					if byte.buttomcombo0.get_active_text() == ' ':
						byte.button0 = None
					else:		
						byte.button0 = byte.buttoncombo0.get_active()

		for byte in self.entryarray:
			if hasattr(byte, 'button1'):
				if widget is byte.buttoncombo1:
					if byte.buttoncombo1.get_active_text() == ' ':
						byte.button1 = None
					else:		
						byte.button1 = byte.buttoncombo1.get_active()


		for byte in self.entryarray:
			if hasattr(byte, 'hat'):
				if widget is byte.hatcombo:
					if byte.hatcombo.get_active_text() == ' ':
						byte.hat = None
					else:		
						byte.hat = byte.hatcombo.get_active()
		
		





























