import window
import threading
import time
import serial
import pygame
import sys
from gi.repository import Gtk, Gdk, GLib



mainwin = window.MainWindow()




def background():
	None


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
pygame.quit()
Gdk.threads_leave()
