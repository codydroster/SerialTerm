import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk




	#Gtk window subclass : main window
class MainWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Serial Term")
		self.set_default_size(800, 400)
		
		
		mainbox = Gtk.Box(orientation='vertical')
		portBox = Gtk.Box(orientation = 'horizontal', spacing = 10)
	
		appmenu = AppMenuBar()	
		mainbox.add(appmenu)
		openDevice = Gtk.Button(label = "Connect")
		openDevice.connect('clicked', self.open_serial)
			
		serialLabel = Gtk.Label("Serial Port:")

		portBox.add(serialLabel)
		


		self.serialPortCombo = Gtk.ComboBoxText()

		self.edit = Gtk.Entry()
		self.edit.set_text('/dev/tty')
		devEntry = self.edit.get_text()
		self.serialPortCombo.add(self.edit)
		self.serialPortCombo.append('0', devEntry)
		self.serialPortCombo.append('1', 'dev1')
		self.serialPortCombo.append('2', 'dev2')
		portBox.add(self.serialPortCombo)		
		self.serialPortCombo.connect('changed', self.dev_port_changed)
		portBox.add(openDevice)
		self.add(mainbox)
		mainbox.add(portBox)

	def open_serial(self, widget):
		
		#print(self.serialPortCombo.get_active_text())
		print(self.edit.get_text())
		
	def dev_port_changed(self, widget):
		self.edit.set_text(self.serialPortCombo.get_active_text())



class ControllerWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Controller")
		self.set_default_size(1200,600)

class SerialWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Open Serial Port")
		self.set_default_size(400,600)
		serialbox = Gtk.Box(orientation = 'vertical', spacing = 10)

		row1 = SerialWindowBox()
		row1.set_label_text("Baudrate:")
		
		serialbox.add(row1)
		sep = Gtk.Separator()
		serialbox.add(sep)
		
		



		self.add(serialbox)
		
		
class SerialWindowBox(Gtk.Box):
	
	def __init__(self):	
		Gtk.Box.__init__(self, orientation='horizontal', spacing=10)
		self.label = Gtk.Label()
		self.add(self.label)
	
		combo = Gtk.ComboBoxText()
		combo.append('0', "9600")
		combo.append('1', "19200")
		combo.append('2', "115200")
	
		self.add(combo)
	


	def set_label_text(self, labelText):	
		self.label.set_text(labelText)

	#Widget classes
class WindowBox(Gtk.Box):
	
	def __init__(self):
		Gtk.Box.__init__(self, orientation='vertical', spacing=10)


class AppMenuBar(Gtk.MenuBar):
	
	def __init__(self):
		Gtk.MenuBar.__init__(self)

		self.controller = ControllerWindow()
		self.serialWin = SerialWindow()
		
		filemenu = Gtk.Menu()

		fileitem = Gtk.MenuItem("File")
		fileitem.set_submenu(filemenu)
		
		exititem = Gtk.MenuItem("exit")
		filemenu.add(exititem)
		
		exititem.connect("activate", Gtk.main_quit)


		
		viewmenu = Gtk.Menu()

		viewitem = Gtk.MenuItem("View")
		viewitem.set_submenu(viewmenu)
		controlleritem = Gtk.MenuItem("Controller")
		
		viewmenu.add(controlleritem)
		controlleritem.connect("activate", self.open_controller)

		optionsItem = Gtk.MenuItem("Serial Port Options")
		viewmenu.add(optionsItem)
		optionsItem.connect("activate", self.open_serial)

		self.add(fileitem)
		self.add(viewitem)

	def open_controller(self, widget):
		
		self.controller.show()

	def open_serial(self, widget):
		
		self.serialWin.show_all()


main = MainWindow()
main.connect("destroy", Gtk.main_quit)
main.show_all()
Gtk.main()



