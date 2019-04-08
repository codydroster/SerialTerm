import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject



class ButtonAttributes():
	
	def __init__(self, name):
		self.name = name
		self.min = 0
		self.max = 10
		self.rawvalue = 0

		self.value = 1
		self.buttoncnt = 0
	
	
	#GTK
		self.box = Gtk.Box(orientation = 'vertical')
		self.boxlab = Gtk.Box(orientation = 'horizontal')


		self.label = Gtk.Label(self.name + ':')
		self.labelval = Gtk.Label()
		self.labelval.set_max_width_chars(10)
		self.label.set_halign(Gtk.Align.START)

		self.labelval.set_halign(Gtk.Align.START)
		self.level = Gtk.LevelBar()
		self.level.set_size_request(150,0)
		self.box.set_margin_left(10)
		self.box.set_margin_right(10)
		self.box.set_margin_top(10)
		self.box.set_margin_bottom(10)
		self.level.set_min_value(0)
		self.level.set_max_value(2)
		self.level.set_value(1)

	
		self.boxlab.add(self.label)
		self.boxlab.add(self.labelval)
		self.box.add(self.boxlab)	
		self.box.add(self.level)


	def get_value(self):

		self.value = self.max * (self.rawvalue)
 		
		return self.value

	def set_levelbar(self, val):

		self.level.set_max_value(abs(self.max))


		self.level.set_value(abs(val))
		self.labelval.set_text(str(self.value))




class AxisAttributes():
	
	def __init__(self, name):
		self.name = name
		self.min = 0
		self.max = 10
		self.rawvalue = 0
		self.inverted = 1
		self.value = 1


#GTK
		self.box = Gtk.Box(orientation = 'vertical')
		self.boxlab = Gtk.Box(orientation = 'horizontal')


		self.label = Gtk.Label(self.name + ': ')
		self.labelval = Gtk.Label()
		self.labelval.set_max_width_chars(12)
		self.labelval.set_halign(Gtk.Align.START)

		self.label.set_halign(Gtk.Align.START)
		self.level = Gtk.LevelBar()
		self.level.set_size_request(150,0)
		self.box.set_margin_left(10)
		self.box.set_margin_right(10)
		self.box.set_margin_top(10)
		self.box.set_margin_bottom(10)
		self.level.set_min_value(0)
		self.level.set_max_value(10)
		self.level.set_value(5)


	
		self.boxlab.add(self.label)
		self.boxlab.add(self.labelval)
		self.box.add(self.boxlab)	
		self.box.add(self.level)


	def get_value(self):

		self.value = self.rawvalue * self.max * self.inverted
		return self.value

	def set_levelbar(self, val):

		self.level.set_max_value(self.max)
		middle = self.max/2
		self.level.set_value(middle + val/2)
		self.labelval.set_text(str(self.value)[:6])



class HatAttributes():
	
	def __init__(self, name):
		self.name = name
		self.min = 0
		self.max = 10
	
		self.rawvalue = 0


		self.inverted = 1
		self.value = 0
		self.buttoncnt = 0

		#GTK
		self.box = Gtk.Box(orientation = 'vertical')
		self.boxlab = Gtk.Box(orientation = 'horizontal')

		self.label = Gtk.Label(self.name + ':')
		self.labelval = Gtk.Label()
		self.label.set_halign(Gtk.Align.START)
		self.level = Gtk.LevelBar()

		self.level.set_size_request(150,0)
		self.box.set_margin_left(10)
		self.box.set_margin_right(10)
		self.box.set_margin_top(10)
		self.box.set_margin_bottom(10)
		self.level.set_min_value(0)
		self.level.set_max_value(10)
		
		self.level.set_value(5)
	
		self.boxlab.add(self.label)
		self.boxlab.add(self.labelval)
		self.box.add(self.boxlab)	
		self.box.add(self.level)

	def get_value(self):
		self.value = self.rawvalue * self.max * self.inverted
		return self.value

	def set_levelbar(self, val):
		
		self.level.set_max_value(abs(self.max))
		middle = self.max/2
		self.level.set_value(middle + val/2)
		
		self.labelval.set_text(str(self.value)[:6])




