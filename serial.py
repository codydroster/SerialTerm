import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk




	#Gtk window subclass : main window
class MainWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Serial Term")
		self.set_default_size(800, 400)
		
		#sub windows
		self.controller = ControllerWindow()

		#serial settings window
		self.serialWin = SerialWindow()
		self.serialWin.connect("delete-event", self.serialWin.delete_event)
		
		self.text2 = Gtk.Entry()  #remove eventually
		self.text2.set_width_chars(40)

		#layout containers
		self.mainbox = Gtk.Box(orientation='vertical', spacing = 6)
		self.portBox = Gtk.Box(orientation = 'horizontal', spacing = 6)
		self.portBox.set_margin_bottom(10)
		self.ser_pb = SerialMainBox()
		self.scrolled_term = ScrolledTerm()
		self.scroll_box = Gtk.Box(orientation = 'vertical')
		self.lastbox = Gtk.Box()
		
		#menubar
		self.appmenu = AppMenuBar()	
		self.mainbox.add(self.appmenu)

		self.scroll_box.add(self.scrolled_term)
		self.scroll_box.add(self.text2)
		

		#Paned Widget		
		self.sep = Gtk.Paned(orientation = 'vertical')
		#self.sep.pack1(self.scrolled_term, resize = True, shrink = True)
		#self.sep.pack2(self.text2, resize = False, shrink = False)
		self.sep.add1(self.scroll_box)
		self.sep.add2(self.lastbox)
		
		#layout: add to main window		
		self.add(self.mainbox)
		self.mainbox.add(self.ser_pb)
		self.mainbox.add(self.sep)
		#self.mainbox.add(self.lastbox)

		



class SerialMainBox(Gtk.Box):
	
	def __init__(self):
		Gtk.Box.__init__(self, spacing = 10)
		
		#initialize
		self.serialPortCombo = Gtk.ComboBoxText()
		self.serialLabel = Gtk.Label(" Serial Port:")
		self.openDevice = Gtk.Button(label = "Connect")
		self.edit = Gtk.Entry()
		self.serial_info_label = Gtk.Label("Info:")
		self.serial_info = Gtk.Label()

		
		#connect
		self.openDevice.connect('clicked', self.open_serial)
		self.serialPortCombo.connect('changed', self.dev_port_changed)
		
		
		#combo box
		self.edit.set_text('/dev/tty')
		self.devEntry = self.edit.get_text()
		self.serialPortCombo.add(self.edit)
		self.serialPortCombo.append('0', self.devEntry)
		self.serialPortCombo.append('1', 'dev1')
		self.serialPortCombo.append('2', 'dev2')
		
		
		#add widgets in order
		self.add(self.serialLabel)
		self.add(self.serialPortCombo)
		self.add(self.openDevice)		
		self.add(self.serial_info_label)
		self.add(self.serial_info)



	def open_serial(self, widget):
		#print(self.serialPortCombo.get_active_text())
		print(self.edit.get_text())

	def dev_port_changed(self, widget):
		self.edit.set_text(self.serialPortCombo.get_active_text())

class ScrolledTerm(Gtk.ScrolledWindow):
	def __init__(self):
		Gtk.ScrolledWindow.__init__(self)

		self.frame = Gtk.Frame()
		self.term_text = Gtk.TextView()
		


		self.set_size_request(100, 300)
		self.set_margin_left(10)
		self.set_margin_right(10)
		self.set_margin_top(10)
		self.set_margin_bottom(10)

		self.add(self.term_text)

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

		
		main.ser_pb.serial_info.set_text(self.serial_info[0] + ', ' + self.serial_info[1] 
								+ '-' + self.serial_info[2][0] + '-' + self.serial_info[3])
		self.hide_on_delete()
		return True



class SerialWindowBox(Gtk.Box):
	
	def __init__(self):	
		Gtk.Box.__init__(self, orientation='horizontal', spacing=10)
		self.combo = Gtk.ComboBoxText()

		self.label = Gtk.Label()
		self.add(self.label)
		self.label.set_width_chars(10)
		self.label.xpad = 2
	

		
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
		
		#initialize
		filemenu = Gtk.Menu()
		viewmenu = Gtk.Menu()

		fileitem = Gtk.MenuItem("File")
		exititem = Gtk.MenuItem("exit")
		viewitem = Gtk.MenuItem("View")
		optionsItem = Gtk.MenuItem("Serial Port Options")
		
		controlleritem = Gtk.MenuItem("Controller")
		
		exititem.connect("activate", Gtk.main_quit)
		controlleritem.connect("activate", self.open_controller)
		optionsItem.connect("activate", self.open_serial)


		fileitem.set_submenu(filemenu)
		filemenu.add(exititem)
		
		
		
		
		
		viewmenu.add(controlleritem)
		viewmenu.add(optionsItem)
		viewitem.set_submenu(viewmenu)
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



