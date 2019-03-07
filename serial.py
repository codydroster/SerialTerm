import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk




	#Gtk window subclass : main window
class MainWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Serial Term")
		self.set_default_size(800, 400)

		self.serial_info_label = Gtk.Label("Info:")

		self.serial_info = Gtk.Label()
		self.controller = ControllerWindow()
		self.serialWin = SerialWindow()
		self.serialWin.connect("delete-event", self.serialWin.delete_event)
		
		mainbox = Gtk.Box(orientation='vertical')
		portBox = Gtk.Box(orientation = 'horizontal', spacing = 6)
	
		appmenu = AppMenuBar()	
		mainbox.add(appmenu)
		openDevice = Gtk.Button(label = "Connect")
		openDevice.connect('clicked', self.open_serial)
			
		serialLabel = Gtk.Label(" Serial Port:")

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

		portBox.add(self.serial_info_label)
		portBox.add(self.serial_info)
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
		self.set_default_size(250,200)
		serialbox = Gtk.Box(orientation = 'vertical', spacing = 10)


		self.row1 = SerialWindowBox()
		self.row1.set_label_text("Baudrate: ")	
		self.row1.combo.append('0', "9600")
		self.row1.combo.append('1', "19200")
		self.row1.combo.append('2', "115200")
		self.row1.combo.set_active_id('0')
		serialbox.add(self.row1)

		self.row2 = SerialWindowBox()	
		self.row2.set_label_text("Data Bits: ")
		self.row2.combo.append('0', '5')
		self.row2.combo.append('1', '6')
		self.row2.combo.append('2', '7')
		self.row2.combo.append('3', '8')
		self.row2.combo.set_active_id('3')
		serialbox.add(self.row2)

		self.row3 = SerialWindowBox()
		self.row3.set_label_text("Parity:       ")
		self.row3.combo.append('0', 'None')
		self.row3.combo.append('1', 'Odd')
		self.row3.combo.append('2', 'Even')
		self.row3.combo.set_active_id('0')
		serialbox.add(self.row3)

		self.row4 = SerialWindowBox()
		self.row4.set_label_text("Stop Bits:  ")
		self.row4.combo.append('0', '1')
		self.row4.combo.append('1', '1.5')
		self.row4.combo.append('2', '2')
		self.row4.combo.set_active_id('0')
		serialbox.add(self.row4)

		self.add(serialbox)

		

			
	def delete_event(self, window, event):
		self.serial_info = [self.row1.combo.get_active_text()]
		self.serial_info.append(self.row2.combo.get_active_text())
		self.serial_info.append(self.row3.combo.get_active_text())
		self.serial_info.append(self.row4.combo.get_active_text())

		
		main.serial_info.set_text(self.serial_info[0] + ', ' + self.serial_info[1] 
								+ '-' + self.serial_info[2][0] + '-' + self.serial_info[3])
		self.hide_on_delete()
		return True



class SerialWindowBox(Gtk.Box):
	
	def __init__(self):	
		Gtk.Box.__init__(self, orientation='horizontal', spacing=10)
		self.label = Gtk.Label()
		self.add(self.label)
		self.label.set_width_chars(10)
		self.label.xpad = 2
	
		self.combo = Gtk.ComboBoxText()

		

	
		self.add(self.combo)
	


	def set_label_text(self, labelText):	
		self.label.set_text(labelText)

	#Widget classes
class WindowBox(Gtk.Box):
	
	def __init__(self):
		Gtk.Box.__init__(self, orientation='vertical', spacing=10)


class AppMenuBar(Gtk.MenuBar):
	
	def __init__(self):
		Gtk.MenuBar.__init__(self)


		
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
		
		main.controller.show()

	def open_serial(self, widget):
	
		main.serialWin.show_all()


main = MainWindow()
main.connect("destroy", Gtk.main_quit)

main.show_all()
Gtk.main()



