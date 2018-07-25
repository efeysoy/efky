import gtk


class Settings(gtk.Window):

    def __init__(self):
        super(Settings, self).__init__()

        self.set_default_size(width=320, height=320)

        # Main panel
        fixed = gtk.Fixed()

        # Left panel
        fixed.put(gtk.Label("Text1"), 5, 5)
        add_button = gtk.Button("Add Module")

        fixed.put(add_button, 5, 300)

        # Right panel
        fixed.put(gtk.Label("Text2"), 165, 5)

        self.add(fixed)
        self.show_all()


    def add_button_clicked(self, widget, data=None):
        x = 5


Settings()
gtk.main()
