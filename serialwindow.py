import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk




BAUDRATE = ('0','300'), ('1','1200'), ('2','2400'), ('3','4800'), ('4','9600'), ('5','19200'), ('6','38400'), ('7','57600'), ('8','115200'), ('9','230400')

DATABITS = ('0','5'), ('1','6'), ('2','7'), ('3','8')

PARITY =  ('0','None'), ('1','Odd'), ('2','Even')

STOPBITS = ('0','1'), ('1','1.5'), ('2','2')


class SerialWindowBox(Gtk.Box):
	
	def __init__(self):	
		Gtk.Box.__init__(self, orientation='horizontal', spacing=10)

		self.combo = Gtk.ComboBoxText()

		self.label = Gtk.Label()
		self.add(self.label)
		self.label.set_width_chars(10)
		self.label.xpad = 2
	

		self.add(self.combo)


class SerialWindow(Gtk.Window):

	
	def __init__(self, title="Serial Port Settings"):
		
		Gtk.Window.__init__(self)
		self.set_default_size(200,200)
		serialbox = Gtk.Box(orientation = 'vertical', spacing = 10)

		self.row1 = SerialWindowBox()
		self.row1.label.set_text("Baudrate:")
		for x, rate in BAUDRATE:
			self.row1.combo.append(x, rate)
		self.row1.combo.set_active_id('0')
		serialbox.add(self.row1)

		self.row2 = SerialWindowBox()	
		self.row2.label.set_text("Data Bits:")
		for x, bits in DATABITS:		
			self.row2.combo.append(x, bits)
		self.row2.combo.set_active_id('3')
		serialbox.add(self.row2)

		self.row3 = SerialWindowBox()
		self.row3.label.set_text("Parity:     ")
		for x, par in PARITY:		
			self.row3.combo.append(x, par)
		self.row3.combo.set_active_id('0')
		serialbox.add(self.row3)

		self.row4 = SerialWindowBox()
		self.row4.label.set_text("Stop Bits:")
		for x, stop in STOPBITS:		
			self.row4.combo.append(x, stop)
		self.row4.combo.set_active_id('0')
		serialbox.add(self.row4)

		
		self.add(serialbox)
