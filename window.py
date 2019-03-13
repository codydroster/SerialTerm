import gi
import serial
import serial.tools.list_ports
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk



#Gtk window subclass : main window
class MainWindow(Gtk.Window):

	

	def __init__(self):
		Gtk.Window.__init__(self, title="Serial Term")
		self.set_default_size(800, 600)

		
		#menubar
		self.appmenu = AppMenuBar()	
		self.level1 = Gtk.LevelBar()
		self.level1.set_min_value(0)
		self.level1.set_max_value(10)
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
		return True

	
	def open_serial(self, widget):
		serialinfo = self.serialportbox.serialinfo
		
		port = self.serialportbox.useport
		port.__init__()
		port.port = self.serialportbox.edit.get_text()
		port.baudrate = int(serialinfo[0])
		port.bytesize = int(serialinfo[1])
		port.parity = serialinfo[2][0]
		port.stopbits = int(serialinfo[3])

		tbuf = self.scrolled_term.term_text.get_buffer()

		try: 
			self.serialportbox.useport.open()
			tbuf.insert_at_cursor('Opened Successfully: ' + port.port + '\n', -1)
			
		except serial.SerialException as err:
			tbuf.insert_at_cursor(format(err) + '\n', -1)
			#self.scrolled_term.termbuffer.insert_at_cursor(format(err), -1)
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

		self.term_text = Gtk.TextView()
		self.term_text.set_editable = True
		self.term_text.set_size_request(100, 200)
		self.sendentry = Gtk.Entry()

		#textterm buffer
		#self.termbuffer = Gtk.TextBuffer()
		#self.termiter = Gtk.TextIter()
		#self.termiter.set_line(10)
			

		self.sendentry.set_width_chars(40)
		self.sendentry.set_margin_left(10)
		self.sendentry.set_margin_right(10)
		self.sendentry.set_margin_bottom(10)
		#self.scrolled_window.set_size_request(100, 200)
		self.scrolled_window.set_propagate_natural_height(True)
		self.scrolled_window.set_margin_left(10)
		self.scrolled_window.set_margin_right(10)
		self.scrolled_window.set_margin_top(10)
		self.scrolled_window.set_margin_bottom(10)

		self.scrolled_window.add(self.term_text)

		self.add(self.scrolled_window)
		self.add(self.sendentry)

class ControllerWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Controller")
		self.set_default_size(600,600)


class SerialWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Open Serial Port")
		self.set_default_size(250,200)
		serialbox = Gtk.Box(orientation = 'vertical', spacing = 10)


		self.row1 = SerialWindowBox()
		self.row1.label.set_text("Baudrate: ")	
		self.row1.combo.append('0', '9600')
		self.row1.combo.append('1', "19200")
		self.row1.combo.append('2', "115200")
		self.row1.combo.set_active_id('0')
		serialbox.add(self.row1)

		self.row2 = SerialWindowBox()	
		self.row2.label.set_text("Data Bits: ")
		self.row2.combo.append('0', '5')
		self.row2.combo.append('1', '6')
		self.row2.combo.append('2', '7')
		self.row2.combo.append('3', '8')
		self.row2.combo.set_active_id('3')
		serialbox.add(self.row2)

		self.row3 = SerialWindowBox()
		self.row3.label.set_text("Parity:       ")
		self.row3.combo.append('0', 'None')
		self.row3.combo.append('1', 'Odd')
		self.row3.combo.append('2', 'Even')
		self.row3.combo.set_active_id('0')
		serialbox.add(self.row3)

		self.row4 = SerialWindowBox()
		self.row4.label.set_text("Stop Bits:  ")
		self.row4.combo.append('0', '1')
		self.row4.combo.append('1', '1.5')
		self.row4.combo.append('2', '2')
		self.row4.combo.set_active_id('0')
		serialbox.add(self.row4)

		self.add(serialbox)

		

			
class SerialWindowBox(Gtk.Box):
	
	def __init__(self):	
		Gtk.Box.__init__(self, orientation='horizontal', spacing=10)
		self.combo = Gtk.ComboBoxText()

		self.label = Gtk.Label()
		self.add(self.label)
		self.label.set_width_chars(10)
		self.label.xpad = 2
	

		self.add(self.combo)
	




class WindowBox(Gtk.Box):
	
	def __init__(self):
		Gtk.Box.__init__(self, orientation='vertical', spacing=10)


class AppMenuBar(Gtk.MenuBar):
	
	def __init__(self):
		Gtk.MenuBar.__init__(self)
		
		#initialize
		filemenu = Gtk.Menu()
		viewmenu = Gtk.Menu()
		self.controller = ControllerWindow()
		self.serialwin = SerialWindow()
		self.pygameins = None

		fileitem = Gtk.MenuItem("File")
		exititem = Gtk.MenuItem("exit")
		viewitem = Gtk.MenuItem("View")
		optionsItem = Gtk.MenuItem("Serial Port Options")
		
		self.controlleritem = Gtk.MenuItem("Controller")
		
		exititem.connect("activate", Gtk.main_quit)
		self.controlleritem.connect("activate", self.open_controller)
		optionsItem.connect("activate", self.open_serial)


		fileitem.set_submenu(filemenu)
		filemenu.add(exititem)
		
		
		viewmenu.add(self.controlleritem)
		viewmenu.add(optionsItem)
		viewitem.set_submenu(viewmenu)
		self.add(fileitem)
		self.add(viewitem)

	def open_controller(self, widget):
		screen = pygame.display.set_mode((400, 400))
		pygame.display.set_caption("Controller")
		#self.controller.show()

	def open_serial(self, widget):
	
		self.serialwin.show_all()






