import window
from gi.repository import Gtk

main = window.MainWindow()
main.connect("destroy", Gtk.main_quit)

main.show_all()
window.Gtk.main()
