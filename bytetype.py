import gi
import pygame

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject



class ConstantValue(Gtk.Box):

	def __init__(self, byte):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 2)
		self.set_margin_left(5)
		self.set_margin_bottom(10)
		
		self.boxtop = Gtk.Box(orientation = 'horizontal', spacing = 5)
		self.boxbot = Gtk.Box(orientation = 'horizontal', spacing = 1)

		self.numbytes = 1
		self.byteval = 0
		self.totalcount = 0



		self.bytenum = Gtk.Label('B ' + str(byte) + ': ')
		self.bytenum.set_markup("<b>" 'B ' + str(byte) + ': ' "</b>")
		
		self.bytenum.set_halign(Gtk.Align(1))
		self.byteentry = Gtk.Entry()
		self.byteentry.set_halign(Gtk.Align(1))
		self.align = Gtk.Alignment()
		self.byteentry.set_placeholder_text('0x00')
		self.byteentry.set_width_chars(6)

		self.boxtop.add(self.bytenum)
	
		self.boxbot.add(self.byteentry)
		self.boxbot.add(self.align)

		self.add(self.boxtop)
		self.add(self.boxbot)

		self.show_all()



		
class ConstantAxis(Gtk.Box):

	def __init__(self, byte):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 2)
		self.set_margin_left(5)
		self.set_margin_bottom(10)

		self.boxtop = Gtk.Box(orientation = 'horizontal', spacing = 5)
		self.boxbot = Gtk.Box(orientation = 'horizontal', spacing = 1)
		

		self.numbytes = 1
		self.byteval = 0
		self.axis = None
		self.totalcount = 0
		self.axistotal = 0

		
		self.button0 = None
		self.button1 = None
		
		self.bytenum = Gtk.Label('B ' + str(byte) + ': ')
		self.bytenum.set_markup("<b>" 'B ' + str(byte) + ': ' "</b>")

		self.byteentry = Gtk.Entry()
		self.byteentry.set_placeholder_text('0x00')
		self.byteentry.set_width_chars(6)


		self.axislab = Gtk.Label('Axis: ')
		self.axislab.set_margin_left(10)
		self.axiscombo = Gtk.ComboBoxText()
		self.axiscombo.set_size_request(40,0)
		
		self.buttonlab = Gtk.Label('Button: ')
		self.buttonlab.set_margin_left(10)
		self.buttoncombo0 = Gtk.ComboBoxText()
		self.buttoncombo0.set_size_request(40,0)
		
		self.buttoncombo1 = Gtk.ComboBoxText()
		self.buttoncombo1.set_size_request(40,0)

		self.boxtop.add(self.bytenum)
		self.boxbot.add(self.byteentry)
		self.boxbot.add(self.axislab)
		self.boxbot.add(self.axiscombo)
		self.boxbot.add(self.buttonlab)
		self.boxbot.add(self.buttoncombo0)
		self.boxbot.add(self.buttoncombo1)
		self.add(self.boxtop)
		self.add(self.boxbot)		
		self.show_all()




class ConstantAxis2B(Gtk.Box):

	def __init__(self, byte):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 2)
		self.set_margin_left(5)
		self.set_margin_bottom(10)

		self.boxtop = Gtk.Box(orientation = 'horizontal', spacing = 5)
		self.boxbot = Gtk.Box(orientation = 'horizontal', spacing = 1)

		self.numbytes = 2
		self.byteval = 0
		self.totalcount = 0
		self.axistotal = 0

		self.axis = None
		self.button0 = None
		self.button1 = None

		self.bytenum = Gtk.Label('B ' + str(byte) + '-' + str(byte + 1) + ': ')
		self.bytenum.set_markup("<b>" 'B ' + str(byte) + '-' + str(byte + 1) + ': ' "</b>")
		self.byteentry = Gtk.Entry()
		self.byteentry.set_placeholder_text('0x00')
		self.byteentry.set_width_chars(6)

		self.axislab = Gtk.Label('Axis: ')
		self.axislab.set_margin_left(10)
		self.axiscombo = Gtk.ComboBoxText()
		self.axiscombo.set_size_request(40,0)

		self.buttonlab = Gtk.Label('Button: ')
		self.buttonlab.set_margin_left(10)
		self.buttoncombo0 = Gtk.ComboBoxText()
		self.buttoncombo0.set_size_request(40,0)


		self.buttoncombo1 = Gtk.ComboBoxText()
		self.buttoncombo1.set_size_request(40,0)

		self.boxtop.add(self.bytenum)
		self.boxbot.add(self.byteentry)
		self.boxbot.add(self.axislab)
		self.boxbot.add(self.axiscombo)
		self.boxbot.add(self.buttonlab)
		self.boxbot.add(self.buttoncombo0)
		self.boxbot.add(self.buttoncombo1)
		self.add(self.boxtop)
		self.add(self.boxbot)

		self.show_all()




class ConstantAxisHat(Gtk.Box):

	def __init__(self, byte):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 2)
		self.set_margin_left(5)
		self.set_margin_bottom(10)

		self.boxtop = Gtk.Box(orientation = 'horizontal', spacing = 5)
		self.boxbot = Gtk.Box(orientation = 'horizontal', spacing = 1)

		self.numbytes = 1
		self.byteval = 0

		self.axis = None
		self.totalcount = 0
		self.axistotal = 0

		
		self.bytenum = Gtk.Label('B ' + str(byte) + ': ')
		self.bytenum.set_markup("<b>" 'B ' + str(byte) + ': ' "</b>")
		self.byteentry = Gtk.Entry()
		self.byteentry.set_placeholder_text('0x00')
		self.byteentry.set_width_chars(6)


		self.axislab = Gtk.Label('Axis: ')
		self.axislab.set_margin_left(10)
		self.axiscombo = Gtk.ComboBoxText()
		self.axiscombo.set_size_request(40,0)
		
		self.hatlabel = Gtk.Label('Hat: ')
		self.hatlabel.set_margin_left(10)
		self.hatcombo = Gtk.ComboBoxText()
		self.hatcombo.set_size_request(40,0)
		
	

		self.boxtop.add(self.bytenum)
		self.boxbot.add(self.byteentry)
		self.boxbot.add(self.axislab)
		self.boxbot.add(self.axiscombo)
		self.boxbot.add(self.hatlabel)
		self.boxbot.add(self.hatcombo)

		self.add(self.boxtop)
		self.add(self.boxbot)

		self.show_all()




class ConstantAxisHat2B(Gtk.Box):

	def __init__(self, byte):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 2)
		self.set_margin_left(5)
		self.set_margin_bottom(10)

		self.boxtop = Gtk.Box(orientation = 'horizontal', spacing = 5)
		self.boxbot = Gtk.Box(orientation = 'horizontal', spacing = 1)

		self.numbytes = 2
		self.byteval = 0
		self.totalcount = 0
		self.axistotal = 0

		self.axis = None
		self.hat = None

		self.bytenum = Gtk.Label('B ' + str(byte) + '-' + str(byte + 1) + ': ')
		self.bytenum.set_markup("<b>" 'B ' + str(byte) + '-' + str(byte + 1) + ': ' "</b>")
		self.byteentry = Gtk.Entry()
		self.byteentry.set_placeholder_text('0x00')
		self.byteentry.set_width_chars(6)

		self.axislab = Gtk.Label('Axis: ')
		self.axislab.set_margin_left(10)
		self.axiscombo = Gtk.ComboBoxText()
		self.axiscombo.set_size_request(40,0)

		self.hatlabel = Gtk.Label('Hat: ')
		self.hatlabel.set_margin_left(10)
		self.hatcombo = Gtk.ComboBoxText()
		self.hatcombo.set_size_request(40,0)


		self.boxtop.add(self.bytenum)
		self.boxbot.add(self.byteentry)
		self.boxbot.add(self.axislab)
		self.boxbot.add(self.axiscombo)
		self.boxbot.add(self.hatlabel)
		self.boxbot.add(self.hatcombo)
		
		self.add(self.boxtop)
		self.add(self.boxbot)
	

		self.show_all()




