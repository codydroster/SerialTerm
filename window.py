import gi
import serial
import serial.tools.list_ports
import time
import pygame

import serialwindow
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk



#Gtk window subclass : main window
class MainWindow(Gtk.Window):

	

	def __init__(self):
		Gtk.Window.__init__(self, title="Serial Term")
		self.set_default_size(800, 600)

		


		#joystick
		self.joystickname = None
		self.joysticklabel = Gtk.Label()

		#menubar
		self.appmenu = AppMenuBar()	
		self.level1 = Gtk.LevelBar()
		self.level1.set_min_value(0)
		self.level1.set_max_value(200)
		self.level1.set_value(3)
		
		

		#layout containers
		self.mainbox = Gtk.Box(orientation='vertical', spacing = 6)
		self.serialportbox = SerialMainBox()
		self.scrolled_term = ScrolledTerm()
		
		#serial settings window
		self.appmenu.serialwin.connect("delete-event", self.delete_event)

		self.serialportbox.opendevice.connect('clicked', self.open_serial)


		
		#layout: add to main window	
		self.mainbox.add(self.appmenu)	
		self.add(self.mainbox)
		self.mainbox.add(self.serialportbox)
		self.mainbox.add(self.scrolled_term)
				
		#self.mainbox.add(self.sep)
		
		self.mainbox.add(self.joysticklabel)
		self.mainbox.add(self.level1)
		
		self.show_all()


	def delete_event(self, window, event):
		serialwin = self.appmenu.serialwin
		serialinfo = self.serialportbox.serialinfo
		serialinfolabel = self.serialportbox.serialinfolabel

		serialinfo[0] = serialwin.row1.combo.get_active_text()
		serialinfo[1] = serialwin.row2.combo.get_active_text()
		serialinfo[2] = serialwin.row3.combo.get_active_text()
		serialinfo[3] = serialwin.row4.combo.get_active_text()

		
		serialinfolabel.set_text(serialinfo[0] + ', '
					+ serialinfo[1] 
					+ '-' + serialinfo[2][0] + '-'
					+ serialinfo[3])
		
		self.appmenu.serialwin.hide_on_delete()


		joyid = self.appmenu.serialwin.controllerbox.contcombo.get_active()
		joysticks = self.appmenu.serialwin.controllerbox.joysticks
		
		if serialwin.controllerbox.contcombo.get_active_text() != None:

			self.joysticklabel.set_label(serialwin.controllerbox.contcombo.get_active_text())
		else:
			self.joysticklabel.set_label("")
		
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
				tbuf.insert_at_cursor('Opened Successfully: ' + port.port + '\n', -1)
				self.scrolled_term.term_text.set_buffer(tbuf)
				self.serialportbox.opendevice.set_label("Close")
				self.scrolled_term.term_text.scroll_to_iter(tbuf.get_end_iter(), 0, False, 0, 0)
			
			except serial.SerialException as err:
				tbuf.insert_at_cursor(format(err) + '\n', -1)
				#self.scrolled_term.termbuffer.insert_at_cursor(format(err), -1)
				self.scrolled_term.term_text.set_buffer(tbuf)
		
		elif self.serialportbox.opendevice.get_label() == "Close":
			
			try:
				self.serialportbox.useport.close()
				tbuf.insert_at_cursor('Closed Successfully' + '\n')
				self.scrolled_term.term_text.set_buffer(tbuf)
				self.serialportbox.opendevice.set_label("Connect")
				self.scrolled_term.term_text.scroll_to_iter(tbuf.get_end_iter(), 0, False, 0, 0)
			
			except serial.SerialException as err:
				tbuf.insert_at_cursor(format(err) + '\n', -1)
				self.scrolled_term.term_text.set_buffer(tbuf)




class SerialMainBox(Gtk.Box):
	
	def __init__(self):
		Gtk.Box.__init__(self, spacing = 10)
		
		#initialize
		seriallabel = Gtk.Label(" Serial Port:")
		info = Gtk.Label("Info:")


		self.serialPortCombo = Gtk.ComboBoxText()
		self.scan = Gtk.Button(label = 'scan')
		self.opendevice = Gtk.Button(label = "Connect")
		self.edit = Gtk.Entry()
		self.serialinfolabel = Gtk.Label()
		
		self.serialinfo = ['9600', '8', 'None', '1']
		self.serialinfolabel.set_text(self.serialinfo[0] + ', '
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
		self.add(seriallabel)
		self.add(self.serialPortCombo)
		self.add(self.scan)
		self.add(self.opendevice)		
		self.add(info)
		self.add(self.serialinfolabel)


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
		self.term_text.set_size_request(100, 300)

		self.sendentry = Gtk.Entry()


			

		self.sendentry.set_width_chars(40)
		self.sendentry.set_margin_left(10)
		self.sendentry.set_margin_right(10)
		self.sendentry.set_margin_bottom(10)

		self.scrolled_window.set_propagate_natural_height(True)
		self.scrolled_window.set_margin_left(10)
		self.scrolled_window.set_margin_right(10)
		self.scrolled_window.set_margin_top(10)
		self.scrolled_window.set_margin_bottom(10)

		self.scrolled_window.add(self.term_text)

		self.add(self.scrolled_window)
		self.add(self.sendentry)








class AppMenuBar(Gtk.MenuBar):
	
	def __init__(self):
		Gtk.MenuBar.__init__(self)
		
		#initialize
		filemenu = Gtk.Menu()
		viewmenu = Gtk.Menu()

		self.serialwin = serialwindow.SerialWindow()
		self.pygameins = None

		fileitem = Gtk.MenuItem("File")
		exititem = Gtk.MenuItem("exit")
		viewitem = Gtk.MenuItem("View")
		optionsItem = Gtk.MenuItem("Settings")
		

		
		exititem.connect("activate", Gtk.main_quit)

		optionsItem.connect("activate", self.open_serial)


		fileitem.set_submenu(filemenu)
		filemenu.add(exititem)
		
		

		viewmenu.add(optionsItem)
		viewitem.set_submenu(viewmenu)
		self.add(fileitem)
		self.add(viewitem)

	def open_serial(self, widget):
	
		self.serialwin.show_all()






	
