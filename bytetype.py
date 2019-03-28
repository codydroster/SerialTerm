import gi
import pygame
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject



class ConstantValue(Gtk.Box):

	def __init__(self, byte):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 5)
		self.set_margin_left(5)
		self.box1 = Gtk.Box(self, orientation = 'horizontal', spacing = 5)
		self.box2 = Gtk.Box(self, orientation = 'horizontal')



		self.numbytes = 1
		self.byteval = 0


		self.bytenum = Gtk.Label('B ' + str(byte) + ': ')
		self.bytenum.set_halign(Gtk.Align(1))
		self.byteentry = Gtk.Entry()
		self.byteentry.set_halign(Gtk.Align(1))
		self.align = Gtk.Alignment()
		self.byteentry.set_placeholder_text('0x00')
		self.byteentry.set_width_chars(6)

	#	self.byteentry.set_margin_left(12)



		self.box1.add(self.byteentry)
		self.box1.add(self.align)
		self.box2.add(self.bytenum)
		self.add(self.box1)
		self.add(self.box2)
		self.show_all()



		
class ConstantAxis(Gtk.Box):

	def __init__(self, byte):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 5)
		self.box1 = Gtk.Box(orientation = 'horizontal', spacing = 5)
		self.box2 = Gtk.Box(orientation = 'horizontal')
		self.set_margin_left(5)
		self.set_margin_right(5)
		self.set_margin_bottom(5)

		self.numbytes = 1
		self.byteval = 0
		self.axis = None
		self.button0 = None
		self.button1 = None
		
		self.bytenum = Gtk.Label('B ' + str(byte) + ': ')
		self.byteentry = Gtk.Entry()
		self.byteentry.set_placeholder_text('0x00')
		self.byteentry.set_width_chars(6)
	#	self.byteentry.set_margin_left(12)

		self.axislab = Gtk.Label('Axis: ')
		self.axiscombo = Gtk.ComboBoxText()
		self.axiscombo.set_size_request(40,0)
		
		self.buttonlab = Gtk.Label('Button: ')
		self.buttoncombo0 = Gtk.ComboBoxText()
		self.buttoncombo0.set_size_request(40,0)
		
		self.buttoncombo1 = Gtk.ComboBoxText()
		self.buttoncombo1.set_size_request(40,0)

		self.box2.add(self.bytenum)
		self.box1.add(self.byteentry)
		self.box1.add(self.axislab)
		self.box1.add(self.axiscombo)
		self.box1.add(self.buttonlab)
		self.box1.add(self.buttoncombo0)
		self.box1.add(self.buttoncombo1)
		self.add(self.box1)
		self.add(self.box2)		
		self.show_all()




class ConstantAxis2B(Gtk.Box):

	def __init__(self, byte):
		Gtk.Box.__init__(self, orientation = 'horizontal', spacing = 5)
		self.set_margin_left(2)
		self.set_margin_right(5)
		self.set_margin_bottom(5)

		self.numbytes = 2
		self.byteval = 0

		self.axis = None
		self.button0 = None
		self.button1 = None

		self.bytenum = Gtk.Label('B ' + str(byte) + '-' + str(byte + 1) + ': ')
		self.byteentry = Gtk.Entry()
		self.byteentry.set_placeholder_text('0x00')
		self.byteentry.set_width_chars(6)

		self.axislab = Gtk.Label('Axis: ')
		self.axiscombo = Gtk.ComboBoxText()
		self.axiscombo.set_size_request(40,0)

		self.buttonlab = Gtk.Label('Button: ')
		self.buttoncombo0 = Gtk.ComboBoxText()
		self.buttoncombo0.set_size_request(40,0)


		self.buttoncombo1 = Gtk.ComboBoxText()
		self.buttoncombo1.set_size_request(40,0)

		self.add(self.bytenum)
		self.add(self.byteentry)
		self.add(self.axislab)
		self.add(self.axiscombo)
		self.add(self.buttonlab)
		self.add(self.buttoncombo0)
		self.add(self.buttoncombo1)
		self.show_all()




class ConstantAxisHat(Gtk.Box):

	def __init__(self, byte):
		Gtk.Box.__init__(self, orientation = 'horizontal', spacing = 5)
		self.set_margin_left(5)
		self.set_margin_right(5)
		self.set_margin_bottom(5)
		self.numbytes = 1
		self.byteval = 0

		self.axis = None
		self.hat = 0
		
		self.bytenum = Gtk.Label('B ' + str(byte) + ': ')
		self.byteentry = Gtk.Entry()
		self.byteentry.set_placeholder_text('0x00')
		self.byteentry.set_width_chars(6)
		self.byteentry.set_margin_left(12)

		self.axislab = Gtk.Label('Axis: ')
		self.axiscombo = Gtk.ComboBoxText()
		self.axiscombo.set_size_request(40,0)
		
		self.hatlabel = Gtk.Label('Hat: ')
		self.hatcombo = Gtk.ComboBoxText()
		self.hatcombo.set_size_request(40,0)
		
	

		self.add(self.bytenum)
		self.add(self.byteentry)
		self.add(self.axislab)
		self.add(self.axiscombo)
		self.add(self.hatlabel)
		self.add(self.hatcombo)

		self.show_all()




class ConstantAxisHat2B(Gtk.Box):

	def __init__(self, byte):
		Gtk.Box.__init__(self, orientation = 'horizontal', spacing = 5)
		self.set_margin_left(5)
		self.set_margin_right(5)
		self.set_margin_bottom(5)
		self.numbytes = 2
		self.byteval = 0

		self.axis = None
		self.hat = None

		self.bytenum = Gtk.Label('B ' + str(byte) + '-' + str(byte + 1) + ': ')
		self.byteentry = Gtk.Entry()
		self.byteentry.set_placeholder_text('0x00')
		self.byteentry.set_width_chars(6)

		self.axislab = Gtk.Label('Axis: ')
		self.axiscombo = Gtk.ComboBoxText()
		self.axiscombo.set_size_request(40,0)

		self.hatlabel = Gtk.Label('Hat: ')
		self.hatcombo = Gtk.ComboBoxText()
		self.hatcombo.set_size_request(40,0)


		self.add(self.bytenum)
		self.add(self.byteentry)
		self.add(self.axislab)
		self.add(self.axiscombo)
		self.add(self.hatlabel)
		self.add(self.hatcombo)
		
		self.show_all()




