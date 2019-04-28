import gi
import pygame
import transmitbyte
import controllerattributes

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject



class ControllerWindow(Gtk.Window):
	def __init__(self):

		Gtk.Window.__init__(self, title="Controller Settings")
		self.set_default_size(1050,750)

		mainbox = Gtk.Box(orientation = 'horizontal', spacing = 10)
		mainbox.set_margin_top(10)
		serialbox = Gtk.Box(orientation = 'vertical', spacing = 10)

		

		sep = Gtk.VSeparator()
		self.controllerbox = ControllerBox()


		self.controllerbox.bytebox.typeadd.connect('clicked', self.map_connect)
		self.controllerbox.endpoint_button_box.entrymax.connect("activate", self.lose_focus)
		self.controllerbox.endpoint_hat_box.entrymax.connect("activate", self.lose_focus)
		self.controllerbox.endpoint_axis_box.entrymax.connect("activate", self.lose_focus)
		
		self.controllerbox.endpoint_axis_box.sumaxisbut.connect("toggled", self.sum_toggled)


		mainbox.add(self.controllerbox)
		self.add(mainbox)


	def sum_toggled(self, widget):
		contcombo = self.controllerbox.contcombo
		inputcombo = self.controllerbox.endpoint_axis_box.inputcombo
		self.controllerbox.butbox.axisattr[contcombo.get_active()][inputcombo.get_active()].sumaxisbool = widget.get_active()
		

			
		

	def lose_focus(self, widget):
		
		self.set_focus(None)
		return True
		

	#connect bytebox entries to lose focus on event: ENTER
	def map_connect(self, widget):
		for ele in self.controllerbox.bytebox.entryarray:
			if hasattr(ele, 'byte_entry'):
				ele.byte_entry.connect("activate", self.lose_focus)

	

class ControllerBox(Gtk.Box):

	def __init__(self):
		Gtk.Box.__init__(self, orientation = 'vertical')
		

		self.joystick2 = None

		contbox = Gtk.Box(orientation = 'horizontal', spacing = 5)
		contbox.set_margin_bottom(20)
		contbox.set_margin_left(10)
		contbox.set_size_request(750,0)
		self.butbox = ButtonBox()
		self.labelbox = Gtk.Box(orientation = 'horizontal')

		contlabel = Gtk.Label("Controller: ")


	#component window
		self.scrollbuttonwindow = Gtk.ScrolledWindow()
		self.scrollbuttonwindow.set_min_content_height(500)

		self.scrollbuttonwindow.set_propagate_natural_width(True)
		self.scrollbuttonwindow.set_size_request(550,0)
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
		self.endpoint_button_box = EndPointBox(label='Button:', typ='button')

		self.endpoint_hat_box = EndPointBox(label='Hat: ', typ='hat')
		self.endpoint_axis_box = EndPointBox(label='Axis:',typ='axis')		


		self.endpoint_button_box.entrymax.connect('focus-out-event', self.update_endpoints)
		self.endpoint_axis_box.entrymax.connect('focus-out-event', self.update_endpoints)
		self.endpoint_hat_box.entrymax.connect('focus-out-event', self.update_endpoints)


		self.endpoint_button_box.inputcombo.connect('changed', self.input_changed)
		self.endpoint_axis_box.inputcombo.connect('changed', self.input_changed)
		self.endpoint_hat_box.inputcombo.connect('changed', self.input_changed)
		
		self.endpoint_axis_box.inputinv.connect('toggled', self.invert)
		self.endpoint_hat_box.inputinv.connect('toggled', self.invert)



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




		self.leftbox.add(self.endpoint_button_box)
		self.leftbox.add(self.endpoint_hat_box)
		self.leftbox.add(self.endpoint_axis_box)
		
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
		endbut = self.endpoint_button_box
		endaxis = self.endpoint_axis_box
		endhat = self.endpoint_hat_box



	#set endpoint

		if widget is endbut.entrymax:
			self.butbox.buttonattr[self.contcombo.get_active()][endbut.inputcombo.get_active()].max = float(endbut.entrymax.get_text())

		elif widget is endaxis.entrymax:
			self.butbox.axisattr[self.contcombo.get_active()][endaxis.inputcombo.get_active()].max = float(endaxis.entrymax.get_text())
	
		elif widget is endhat.entrymax:
			self.butbox.hatattr[self.contcombo.get_active()][endhat.inputcombo.get_active()].max = float(endhat.entrymax.get_text())

		

	def input_changed(self, widget):
		endbut = self.endpoint_button_box
		endaxis = self.endpoint_axis_box
		endhat = self.endpoint_hat_box

		#button
		if widget is endbut.inputcombo:
			endbut.entrymax.set_text(str(self.butbox.buttonattr[self.contcombo.get_active()][endbut.inputcombo.get_active()].max))

		#axis
		if widget is endaxis.inputcombo:
			endaxis.entrymax.set_text(str(self.butbox.axisattr[self.contcombo.get_active()][endaxis.inputcombo.get_active()].max))
			endaxis.sumaxisbut.set_active(self.butbox.axisattr[self.contcombo.get_active()][endaxis.inputcombo.get_active()].sumaxisbool)
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
		endaxis = self.endpoint_axis_box
		endhat = self.endpoint_hat_box

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
		self.butbox.map()

		self.endpoint_button_box.attr = self.butbox.buttonattr
		self.endpoint_axis_box.attr = self.butbox.axisattr
		self.endpoint_hat_box.attr = self.butbox.hatattr
		
		self.endpoint_button_box.joystickid = self.contcombo.get_active()
		self.endpoint_axis_box.joystickid = self.contcombo.get_active()
		self.endpoint_hat_box.joystickid = self.contcombo.get_active()

		self.endpoint_button_box.map()
		self.endpoint_axis_box.map()
		self.endpoint_hat_box.map()

		self.bytebox.map_transmitbyte_box()


		pygame.joystick.init()
		self.joystick2 = pygame.joystick.Joystick(widget.get_active())

class ButtonBox(Gtk.Box):
	
	def __init__(self):
		Gtk.Box.__init__(self, orientation = 'horizontal', spacing = 5)

		
		self.joystickid = None
		buttonlabel = Gtk.Label("Buttons: ")
		

		self.buttonbox = []
		self.hatbox = []
		self.axisbox = []


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

		
		#buttonattr

			self.buttonattr.append([])

			self.buttonbox.insert(j, Gtk.Box(orientation = 'vertical'))
			for i in range(joy.get_numbuttons()):
				self.buttonattr[j].insert(i, controllerattributes.ButtonAttributes(name = str(i)))
				self.buttonbox[j].add(self.buttonattr[j][i].box)


	
		#axisattr

			self.axisattr.append([])

			self.axisbox.insert(j, Gtk.Box(orientation = 'vertical'))
			for i in range(joy.get_numaxes()):
				self.axisattr[j].insert(i, controllerattributes.AxisAttributes(name = str(i)))	
				self.axisbox[j].add(self.axisattr[j][i].box)


	
		#hatattr

			self.hatattr.append([])

			self.hatbox.insert(j, Gtk.Box(orientation = 'vertical'))
			for i in range(joy.get_numhats()+1):
				self.hatattr[j].insert(i, controllerattributes.HatAttributes(name = str(i)))
				self.hatbox[j].add(self.hatattr[j][i].box)




	def map(self):

		self.show_all()
		
	#buttonbox
		for box in self.buttonbox:
			if box in self.get_children():
				self.remove(box)

		for i in range(pygame.joystick.get_count()):
			
			if self.joystickid == i:
				self.add(self.buttonbox[i])
				self.show_all()

	
	#hatbox
		for box in self.hatbox:
			if box in self.get_children():
				self.remove(box)

		for i in range(pygame.joystick.get_count()):
			
			if self.joystickid == i:
				self.add(self.hatbox[i])
				self.show_all()

	#axisbox
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
		
		if typ == 'axis':
			self.sumaxisbut = Gtk.ToggleButton(label = 'SUM AXIS')
			self.add(self.sumaxisbut)
		
		

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
		self.typebox_combo = Gtk.ComboBoxText()
		self.typebox_combo.set_size_request(100,0)
		
		self.num_bytes_combo = Gtk.ComboBoxText()
		self.num_bytes_combo.set_size_request(50,0)
		
		self.typeadd = Gtk.Button(label = 'ADD')

		self.typeadd.connect('clicked', self.add_byte)
		self.entryarray = []



	#current joystick
		self.joystickid = None
		
	#byte types
		self.typebox_combo.insert_text(0, "Constant")
		self.typebox_combo.insert_text(1, "Axis + Button")
		self.typebox_combo.insert_text(2, "Axis + Hat")

		self.typebox_combo.set_active(0)

		self.num_bytes_combo.insert_text(0, "1 Byte")
		self.num_bytes_combo.insert_text(1, "2 Byte")
		self.num_bytes_combo.set_active(0)

		self.headerbox.add(self.typelabel)
		self.headerbox.add(self.typebox_combo)
		self.headerbox.add(self.num_bytes_combo)
		self.headerbox.add(self.typeadd)
		self.add(self.headerbox)



	def map_transmitbyte_box(self):
		for val in self.entryarray:
			if hasattr(val, 'axis_combo'):
				val.axis_combo.remove_all()

				if self.joystickid != -1:
					if self.joystickid != None:

						for i in range(pygame.joystick.Joystick(self.joystickid).get_numaxes()):
							val.axis_combo.insert_text(i, str(i))
						val.axis_combo.insert_text(-1, ' ')



			if hasattr(val, 'button_label'):
				val.button0_combo.remove_all()
				val.button1_combo.remove_all()
				
				if self.joystickid != -1:
					if self.joystickid != None:

						for i in range(pygame.joystick.Joystick(self.joystickid).get_numbuttons()):
							val.button0_combo.insert_text(i, str(i))
							val.button1_combo.insert_text(i, str(i))
						val.button0_combo.insert_text(-1, ' ')
						val.button1_combo.insert_text(-1, ' ')



			if hasattr(val, 'hat_label'):
				val.hat_combo.remove_all()

				if self.joystickid != -1:
					if self.joystickid != None:

						for i in range(pygame.joystick.Joystick(self.joystickid).get_numhats()+1):
							val.hat_combo.insert_text(i, str(i))
						val.hat_combo.insert_text(-1, ' ')



#adds byte to be transmitted to gui

	def add_byte(self, widget):
		byteindex = 0
		for byte in self.entryarray:
			byteindex += byte.numbytes
			

		if self.typebox_combo.get_active() == 0:
				
				
			currentbyte = transmitbyte.TransmitByte('Constant', (self.num_bytes_combo.get_active() + 1), byteindex)
			self.entryarray.append(currentbyte)
			self.add(currentbyte)
			
	#update on focus-out
			currentbyte.byte_entry.connect('focus-out-event', self.update_entry)
	
			

		if self.typebox_combo.get_active() == 1:
	
			currentbyte = transmitbyte.TransmitByte('Button', (self.num_bytes_combo.get_active() + 1), byteindex)
			self.entryarray.append(currentbyte)
			
			
			currentbyte.byte_entry.connect('focus-out-event', self.update_entry)
			currentbyte.axis_combo.connect('changed', self.update_transmitbyte_arguments)
			currentbyte.button0_combo.connect('changed', self.update_transmitbyte_arguments)
			currentbyte.button1_combo.connect('changed', self.update_transmitbyte_arguments)
	
			self.add(currentbyte)

		

		if self.typebox_combo.get_active() == 2:

			currentbyte = transmitbyte.TransmitByte('Hat', (self.num_bytes_combo.get_active() + 1), byteindex)
			self.entryarray.append(currentbyte)

			currentbyte.byte_entry.connect('focus-out-event', self.update_entry)
			currentbyte.axis_combo.connect('changed', self.update_transmitbyte_arguments)
			currentbyte.hat_combo.connect('changed', self.update_transmitbyte_arguments)
		
			self.add(currentbyte)
			

			
		
		self.map_transmitbyte_box()




	def update_entry(self, widget, event):
		for byte in self.entryarray:
			if widget is byte.byte_entry:
				try:
					byte.byteval = int(byte.byte_entry.get_text(), 0)
					
				except:
					byte.byteval = 0




	def update_transmitbyte_arguments(self, widget):
	
		for byte in self.entryarray:
			if hasattr(byte, 'axis_combo'):
				if widget is byte.axis_combo:
					if byte.axis_combo.get_active_text() == ' ':
						byte.axis = None
					else:				
						byte.axis = byte.axis_combo.get_active()


			if hasattr(byte, 'button0'):
				if widget is byte.button0_combo:
					if byte.button0_combo.get_active_text() == ' ':
						byte.button0 = None
					else:		
						byte.button0 = byte.button0_combo.get_active()

		
			if hasattr(byte, 'button1'):
				if widget is byte.button1_combo:
					if byte.button1_combo.get_active_text() == ' ':
						byte.button1 = None
					else:		
						byte.button1 = byte.button1_combo.get_active()


		
			if hasattr(byte, 'hat_combo'):
				if widget is byte.hat_combo:
					if byte.hat_combo.get_active_text() == ' ':
						byte.hat = None
					else:		
						byte.hat = byte.hat_combo.get_active()
		
		





























