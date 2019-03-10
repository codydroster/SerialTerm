import window
import threading
import time
import serial
from gi.repository import Gtk, Gdk, GLib



mainwin = window.MainWindow()

def background():
	i = 1
	while True:
		#print(i)
		i = i + 1
		time.sleep(1)
		mainwin.var1 +=1
		#print(mainwin.var1)



mainwin.connect("destroy", Gtk.main_quit)
#main.connect("destroy", Gtk.main_quit)
#main.show_all()

thread1 = threading.Thread(target=background)
thread1.daemon = True






GLib.threads_init()
Gdk.threads_init()
Gdk.threads_enter()
thread1.start()
window.Gtk.main()
Gdk.threads_leave()
