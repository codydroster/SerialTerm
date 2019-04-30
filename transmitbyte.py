import gi
import pygame

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject






# b_type:
#	'Constant'
#	'Button'
#	'Hat'	


class TransmitByte(Gtk.Box):

	def __init__(self, b_type, b_num, index):
		Gtk.Box.__init__(self, orientation = 'vertical', spacing = 2)
		self.set_margin_left(5)
		self.set_margin_bottom(10)

		self.boxtop = Gtk.Box(orientation = 'horizontal', spacing = 5)
		self.boxbot = Gtk.Box(orientation = 'horizontal', spacing = 1)
		
		self.numbytes = b_num
		
		self.byteval = 0

					
		self.byte_entry = Gtk.Entry()
		self.byte_entry.set_width_chars(6)
		
		
		if self.numbytes == 1:
			self.bytenum_label = Gtk.Label('B ' + str(index) + ': ')
			self.bytenum_label.set_markup("<b>" 'B ' + str(index) + ': ' "</b>")
			self.maxval = 0xff
			self.byte_entry.set_placeholder_text('0x00')
			
		elif self.numbytes == 2:
			self.bytenum_label = Gtk.Label('B ' + str(index) + '-' + str(index + 1) + ': ')
			self.bytenum_label.set_markup("<b>" 'B ' + str(index) + '-' + str(index + 1) + ': ' "</b>")
			self.maxval = 0xffff
			self.byte_entry.set_placeholder_text('0x0000')

			
			
				
#populate box

		self.boxtop.add(self.bytenum_label)
		self.boxbot.add(self.byte_entry)
		
		
		
		if b_type != 'Constant':
			self.axis_label = Gtk.Label('Axis: ')
			self.axis_label.set_margin_left(10)
			self.axis_combo = Gtk.ComboBoxText()
			self.axis_combo.set_size_request(40,0)
		
			self.axis_total = 0
		
		#box add
			self.boxbot.add(self.axis_label)
			self.boxbot.add(self.axis_combo)
		
		
		if b_type == 'Button':
			self.button_label = Gtk.Label('Button: ')
			self.button_label.set_margin_left(10)
			self.button0_combo = Gtk.ComboBoxText()
			self.button0_combo.set_size_request(40,0)
			
			self.button1_combo = Gtk.ComboBoxText()
			self.button1_combo.set_size_request(40,0)
			
			self.button0 = None
			self.button1 = None
			self.button_total = 0
			
		#box add
			self.boxbot.add(self.button_label)
			self.boxbot.add(self.button0_combo)
			self.boxbot.add(self.button1_combo)
		
		
		if b_type == 'Hat':
			self.hat_label = Gtk.Label('Hat: ')
			self.hat_label.set_margin_left(10)
			self.hat_combo = Gtk.ComboBoxText()
			self.hat_combo.set_size_request(40,0)
			
			self.hat_total = 0
			self.hat = None
		
		
		#box add
			self.boxbot.add(self.hat_label)
			self.boxbot.add(self.hat_combo)
		
		
		self.add(self.boxtop)
		self.add(self.boxbot)
		
		self.show_all()
		
		
		
class ButtonByte(Gtk.Box):

		def __init__(self, index):
			Gtk.Box.__init__(self, orientation = 'vertical', spacing = 2)
			self.set_margin_left(5)
			self.set_margin_bottom(10)
		
		
			self.boxtop = Gtk.Box(orientation = 'horizontal', spacing = 5)
			self.boxbot = Gtk.Box(orientation = 'horizontal', spacing = 1)
		
		
			self.numbytes = 1
		
			self.byte_entry = Gtk.Entry()
			self.byte_entry.set_placeholder_text('01234567')
			self.byte_entry.set_width_chars(8)
			self.byte_entry.set_max_width_chars(8)
			self.byte_entry.set_max_length(8)
		
			

			self.bytenum_label = Gtk.Label('B ' + str(index) + ': ')
			self.bytenum_label.set_markup("<b>" 'B ' + str(index) + ': ' "</b>")
			self.maxval = 0xff

			
			
			self.boxtop.add(self.bytenum_label)
			self.boxbot.add(self.byte_entry)
			
			self.add(self.boxtop)
			self.add(self.boxbot)
			
			self.show_all()
			
			
			
			
			
			
			
		
		

