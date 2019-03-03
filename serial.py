import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk




	#Gtk window subclass : main window
class MainWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Serial Term")
		self.set_default_size(800, 400)
		
		
		


		mainbox = Gtk.Box(orientation='vertical')

	
		appmenu = AppMenuBar()	
		mainbox.add(appmenu)
	
		self.add(mainbox)
		

		
class ControllerWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Controller")
		self.set_default_size(1200,600)

		


	#Widget classes
class WindowBox(Gtk.Box):
	
	def __init__(self):
		Gtk.Box.__init__(self, orientation='vertical', spacing=10)


class AppMenuBar(Gtk.MenuBar):
	
	def __init__(self):
		Gtk.MenuBar.__init__(self)

		self.controller = ControllerWindow()
		
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


		self.add(fileitem)
		self.add(viewitem)

	def open_controller(self, widget):
		
		self.controller.show()


main = MainWindow()
main.connect("destroy", Gtk.main_quit)
main.show_all()
Gtk.main()






