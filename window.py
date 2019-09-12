import gi
import serial
import serial.tools.list_ports
import pygame

import controllerwindow
import serialwindow
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk



#Gtk window subclass : main window
class MainWindow(Gtk.Window):



	def __init__(self):
		Gtk.Window.__init__(self, title="UART Gamepad")
		self.set_default_size(800, 600)


		self.values = []


		#joystick
		self.joystickname = None
		self.joysticklabel = Gtk.Label()


		#menubar
		self.appmenu = AppMenuBar()




		#layout containers
		self.mainbox = Gtk.Box(orientation='vertical', spacing = 6)

		self.serialportbox = SerialMainBox()
		self.scrolled_term = ScrolledTerm()
		self.bytevalbox = ByteValBox()


		#serial settings window
		self.appmenu.controllerwin.connect("delete-event", self.delete_controller)
		self.appmenu.serialwin.connect("delete-event", self.delete_serial)
		self.serialportbox.opendevice.connect('clicked', self.open_serial)


		#send manual serial entry
		self.scrolled_term.send_button.connect("clicked", self.send_serial_line)
		self.scrolled_term.send_entry.connect("activate", self.send_serial_line)


		#layout: add to main window
		self.mainbox.add(self.appmenu)
		self.add(self.mainbox)
		self.mainbox.add(self.serialportbox)
		self.mainbox.add(self.scrolled_term)

		#self.mainbox.add(self.sep)

		self.mainbox.add(self.joysticklabel)


		self.mainbox.add(self.bytevalbox)



		self.show_all()


	def delete_serial(self, window, event):
		serialwin = self.appmenu.serialwin
		serialinfo = self.serialportbox.serialinfo
		serialinfo_label = self.serialportbox.serialinfo_label



		serialinfo[0] = serialwin.row1.combo.get_active_text()
		serialinfo[1] = serialwin.row2.combo.get_active_text()
		serialinfo[2] = serialwin.row3.combo.get_active_text()
		serialinfo[3] = serialwin.row4.combo.get_active_text()


		serialinfo_label.set_text(serialinfo[0] + ', '
					+ serialinfo[1]
					+ '-' + serialinfo[2][0] + '-'
					+ serialinfo[3])

		serialwin.hide_on_delete()



		return True

	def delete_controller(self, window, event):
		controllerwin = self.appmenu.controllerwin


		if controllerwin.controllerbox.contcombo.get_active_text() != None:

			self.joysticklabel.set_label(controllerwin.controllerbox.contcombo.get_active_text())
		else:
			self.joysticklabel.set_label("")


		controllerwin.hide_on_delete()
		self.bytevalbox.entryarray = self.appmenu.controllerwin.controllerbox.bytebox.entryarray
		self.bytevalbox.map()

		return True


	def open_serial(self, widget):

		tbuf = self.scrolled_term.term_text.get_buffer()

		if self.serialportbox.opendevice.get_label() == "Connect":

			serialinfo = self.serialportbox.serialinfo

			port = self.serialportbox.useport
			port.__init__()
			port.port = self.serialportbox.edit.get_text()
			port.baudrate = int(serialinfo[0])
			port.bytesize = int(serialinfo[1])
			port.parity = serialinfo[2][0]
			port.stopbits = int(serialinfo[3])



			try:
				self.serialportbox.useport.open()
				self.scrolled_term.insert_text_term('Opened Successfully: ' + port.port)
				self.scrolled_term.term_text.scroll_to_iter(tbuf.get_end_iter(), 0, False, 0, 0)
				self.serialportbox.opendevice.set_label("Close")

			except serial.SerialException as err:
				self.scrolled_term.insert_text_term(format(err))



		elif self.serialportbox.opendevice.get_label() == "Close":

			try:
				self.serialportbox.useport.close()
				self.scrolled_term.insert_text_term('Closed Successfully')
				self.serialportbox.opendevice.set_label("Connect")
				self.scrolled_term.term_text.scroll_to_iter(tbuf.get_end_iter(), 0, False, 0, 0)

			except serial.SerialException as err:

				self.scrolled_term.insert_text_term(format(err))



	def send_serial_line(self, widget):
		port = self.serialportbox.useport
		entry = list(self.scrolled_term.send_entry.get_text())

	##byte
		if('0x' in "".join(entry)):
			if (len(entry[2:]) == 1):
				entry.insert(2, '0')

			entry = "".join(entry)
			while('0x' in entry):
				entry = entry[:entry.find('0x')] + entry[entry.find('0x')+2:]
			try:
				port.write(bytes.fromhex(entry))
				if(self.scrolled_term.hex_display_switch.get_active()):
					self.scrolled_term.insert_text_term('TX: ' + entry.upper())
				else:
					entry = "".join(entry)
					self.scrolled_term.insert_text_term('TX: ' + bytes.fromhex(entry).decode())
			except:
				self.scrolled_term.insert_text_term('error')
	##string
		else:
			entry = "".join(entry)
			entry = entry.encode()
			port.write(entry)
			if(self.scrolled_term.hex_display_switch.get_active()):
				self.scrolled_term.insert_text_term('TX: ' + entry.hex().upper())
			else:
				self.scrolled_term.insert_text_term('TX: ' + entry.decode())

class SerialMainBox(Gtk.Box):

	def __init__(self):
		Gtk.Box.__init__(self, spacing = 10)

		#initialize
		serial_label = Gtk.Label()
		serial_label.set_margin_left(6)
		serial_label.set_markup("<b>" 'SerialPort:'  "</b>")
		info_label = Gtk.Label("Info:")
		info_label.set_markup("<b>" 'Info:'  "</b>")

		self.serialPortCombo = Gtk.ComboBoxText()
		self.scan = Gtk.Button(label = 'scan')
		self.opendevice = Gtk.Button(label = "Connect")
		self.edit = Gtk.Entry()
		self.serialinfo_label = Gtk.Label()

		self.serialinfo = ['115200', '8', 'None', '1']
		self.serialinfo_label.set_text(self.serialinfo[0] + ', '
						+ self.serialinfo[1]
						+ '-' + self.serialinfo[2][0] + '-'
						+ self.serialinfo[3])

		#serial initialize
		self.availports = serial.tools.list_ports.comports()
		self.useport = serial.Serial()

		#connect
		self.serialPortCombo.connect('changed', self.dev_port_changed)
		self.scan.connect('clicked', self.pop_down)

		#combo box
		self.edit.set_text('/dev/tty')
		self.devEntry = self.edit.get_text()
		self.serialPortCombo.add(self.edit)
		self.serialPortCombo.append('0', self.devEntry)



		#add widgets in order
		self.add(serial_label)
		self.add(self.serialPortCombo)
		self.add(self.scan)
		self.add(self.opendevice)
		self.add(info_label)
		self.add(self.serialinfo_label)


	def pop_down(self, widget):
		self.serialPortCombo.remove_all()
		self.availports = serial.tools.list_ports.comports()

		for i, port in enumerate(self.availports):
			self.serialPortCombo.insert_text(i, port.device)





	def dev_port_changed(self, widget):
		if  self.serialPortCombo.get_active_text() is not None:
			self.edit.set_text(self.serialPortCombo.get_active_text())



class ScrolledTerm(Gtk.Box):
	def __init__(self):
		Gtk.Box.__init__(self, orientation = 'vertical')

		self.scrolled_window = Gtk.ScrolledWindow()
		self.scrolled_window.set_max_content_height(300)


		self.term_text = Gtk.TextView()
		self.term_text.set_cursor_visible(False)
		self.term_text.set_editable(False)
		self.term_text.set_size_request(100, 300)


		self.entry_box = Gtk.Box(orientation = 'horizontal')
		self.entry_box.set_margin_bottom(15)
		self.send_entry = Gtk.Entry()
		self.send_button = Gtk.Button(label = 'SEND')

		self.send_entry.set_width_chars(48)
		self.send_entry.set_placeholder_text('eg. 0x42 0x4242 hello')
		self.send_entry.set_margin_left(10)
		self.send_entry.set_margin_right(10)





		self.transmitctrl_label = Gtk.Label()
		self.transmitctrl_label.set_markup("<b>" 'CONTROLLER TRANSMIT:'  "</b>")
		self.transmitctrl_label.set_margin_left(20)

		self.hex_display_label = Gtk.Label()
		self.hex_display_label.set_markup("<b>" 'HEX:'  "</b>")
		self.hex_display_label.set_margin_left(10)
		self.hex_display_label.set_margin_right(5)

		self.transmitctrl_switch = Gtk.Switch()
		self.hex_display_switch = Gtk.Switch()

		self.transmitctrl_switch.set_margin_left(10)
		self.transmitctrl_switch.set_margin_right(5)



		self.scrolled_window.set_propagate_natural_height(True)
		self.scrolled_window.set_margin_left(10)
		self.scrolled_window.set_margin_right(10)
		self.scrolled_window.set_margin_top(10)
		self.scrolled_window.set_margin_bottom(10)

		self.scrolled_window.add(self.term_text)
		self.add(self.scrolled_window)
		self.entry_box.add(self.send_entry)
		self.entry_box.add(self.send_button)
		self.entry_box.add(self.hex_display_label)
		self.entry_box.add(self.hex_display_switch)
		self.entry_box.add(self.transmitctrl_label)
		self.entry_box.add(self.transmitctrl_switch)
		self.add(self.entry_box)


	def insert_text_term(self, text):
		tbuf = self.term_text.get_buffer()
		tbuf.insert(tbuf.get_end_iter(), text + '\n', -1)
		self.term_text.set_buffer(tbuf)




class ByteValBox(Gtk.Box):

	def __init__(self):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 25)
		self.set_margin_top(20)
		self.set_margin_left(5)
		self.valbox = []
		self.valrow = []
		self.mainwin_vals = []
		self.entryarray = None



	def map(self):
		for val in self.valbox:

			val.destroy()

		for val in self.valrow:
			val.destroy()


		self.mainwin_vals = []
		self.valbox = []
		self.valrow = []

		for i, val in enumerate(self.entryarray):
			self.mainwin_vals.append([])
			self.mainwin_vals[i].append(Gtk.Label(val.bytenum_label.get_text()))
			self.mainwin_vals[i][0].set_markup("<b>" + val.bytenum_label.get_text() + "</b>")

			self.mainwin_vals[i].append(Gtk.Label(''))


		for i in range(int(len(self.mainwin_vals)/6) + 1):
			self.valrow.append(Gtk.Box(orientation = 'horizontal'))



		for i, val in enumerate(self.mainwin_vals):

			self.valbox.append(Gtk.Box(orientation = 'horizontal'))
			self.valbox[i].add(val[0])
			self.valbox[i].add(val[1])
			self.valbox[i].set_size_request(120,0)
			self.valrow[int(i/6)].add(self.valbox[i])


		for row in self.valrow:
			self.add(row)

		self.show_all()


class AppMenuBar(Gtk.MenuBar):

	def __init__(self):
		Gtk.MenuBar.__init__(self)

		#initialize
		filemenu = Gtk.Menu()
		viewmenu = Gtk.Menu()
		optionsmenu = Gtk.Menu()
		self.controllerwin = controllerwindow.ControllerWindow()

		self.serialwin = serialwindow.SerialWindow()


		fileitem = Gtk.MenuItem("File")
		exititem = Gtk.MenuItem("exit")
		viewitem = Gtk.MenuItem("View")
		controlleritem = Gtk.MenuItem("Controller")
		serialitem = Gtk.MenuItem("Serial")
		clearitem = Gtk.MenuItem("Reset Values")

		optionsitem = Gtk.MenuItem("Options")

		exititem.connect("activate", Gtk.main_quit)

		controlleritem.connect("activate", self.open_cont)
		serialitem.connect("activate", self.open_serial)
		clearitem.connect("activate", self.clear_val)



		fileitem.set_submenu(filemenu)
		filemenu.add(exititem)




		viewmenu.add(controlleritem)
		viewmenu.add(serialitem)
		viewitem.set_submenu(viewmenu)

		optionsitem.set_submenu(optionsmenu)
		optionsmenu.add(clearitem)


		self.add(fileitem)
		self.add(viewitem)
		self.add(optionsitem)

	def clear_val(self, widget):
		controllerbox = self.controllerwin.controllerbox
		for value in controllerbox.bytebox.entryarray:
			if hasattr(value, 'axis_total'):
				value.axis_total = 0

			if hasattr(value, 'button_total'):
				value.button_total = 0

			if hasattr(value, 'hat_total'):
				value.hat_total = 0




	def open_cont(self, widget):

		self.controllerwin.show_all()

	def open_serial(self, widget):

		self.serialwin.show_all()
