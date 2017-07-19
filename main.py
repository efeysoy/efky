# --==============================================================================
# --                            main.py
# --
# --  Date    : 16.08.2016
# --  Author  : efeysoy
# --  Version : v0.1
# --  License : Distributed under the terms of GNU GPL version 2 or later
# --
# --==============================================================================

import pygtk
import gtk, glib, sys, cairo
import importlib
from config import Config
from efky_helper import EfkyHelper

pygtk.require('2.0')
root = None
win = None


def print_me():
    print("ok")


def expose(widget, event):
    cr = widget.window.cairo_create()

    # Sets the operator to clear which deletes everything below where an object is drawn
    cr.set_operator(cairo.OPERATOR_CLEAR)
    # Makes the mask fill the entire window
    cr.rectangle(0.0, 0.0, *widget.get_size())
    # Deletes everything in the window (since the compositing operator is clear and mask fills the entire window
    cr.fill()
    # Set the compositing operator back to the default
    cr.set_operator(cairo.OPERATOR_OVER)

    cr.set_source_rgba(0.2, 0.3, 0.4, .5)
    cr.rectangle(0.0, 0.0, *widget.get_size())
    cr.fill()

    root.draw_all(cr)


def main(argc):
    global root
    global win
    width = 0
    height = 0

    cfg = readconfig()

    if len(cfg.root.width) > 2 and cfg.root.width[-2:] == "px":
        width = int(cfg.root.width[:-2])
    elif len(cfg.root.width) > 1 and cfg.root.width[-1:] == "%":
        width = int(gtk.gdk.screen_get_default().get_width() * (float(cfg.root.width[:-1]) / 100))

    if len(cfg.root.height) > 2 and cfg.root.height[-2:] == "px":
        height = int(cfg.root.height[:-2])
    elif len(cfg.root.height) > 1 and cfg.root.height[-1:] == "%":
        height = int(gtk.gdk.screen_get_default().get_height() * (float(cfg.root.height[:-1]) / 100))
    root.height = height
    root.width = width
    root.x = int(cfg.root.x)
    root.y = int(cfg.root.y)
    root.calculate_sizes()

    win = gtk.Window()
    win.set_keep_below(setting=1)  # keep window under other windows

    win.set_decorated(False)
    # Makes the window paintable, so we can draw directly on it
    win.set_app_paintable(True)

    win.set_size_request(root.width, root.height)
    win.move(root.x, root.y)

    # This sets the windows colormap, so it supports transparency.
    # This will only work if the wm support alpha channel
    screen = win.get_screen()
    win.stick()
    rgba = screen.get_rgba_colormap()
    win.set_colormap(rgba)

    win.connect("destroy", gtk.main_quit)
    win.connect('expose-event', expose)
    glib.timeout_add(int(cfg.root.refreshrate), on_timer)

    size = win.get_size()
    bitmap = gtk.gdk.Pixmap(None, size[0], size[1], 1)
    cr = bitmap.cairo_create()
    cr.set_source_rgba(0.0,0.0,0.0,0.0)
    cr.rectangle((0,0)+size)
    cr.fill()

    win.input_shape_combine_mask(bitmap, 0, 0)

    win.show()
    gtk.main()


def on_timer():
    win.queue_draw()
    return True


def readconfig():
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cfg = Config(file(dir_path + '/efkyrc'))
    __create_nodes(cfg.root)
    return cfg


def __create_nodes(conf, node = None):
    new_node = Node(conf.name)
    if node is not None:  # not root node, so must have a parent
        node.add_node(new_node)
    else:
        global root
        root = new_node
    if hasattr(conf, 'nodes'):
        for i in range(len(conf.nodes)):
            __create_nodes(conf.nodes[i], new_node)


class Node:
    # only root, horizontal and vertical nodes can have node list
    def __init__(self, module):
        self.size_calculated = False
        self.__nodes = []
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.padding = 0
        self.ratio = (0, 0)  # width, height ratio
        self.non_rel_ratio = (0, 0) # ratios re calculated by other elements, this ratio will not be changed
        self.name = module
        self.module = ""
        if module != "root" and module != "vertical" and module != "horizontal":
            self.module = importlib.import_module(module)
            try:
                self.module.efky_init()
            except AttributeError:
                print("Module " + module + " doesn't have an initializer.")

    def add_node(self, node):
        self.__nodes.append(node)

    def calculate_sizes(self):
        self.__calculate_real_ratios()
        self.__calculate_sizes()
        self.__calculate_locations()

    def __calculate_locations(self):
        tmp_x = self.x
        tmp_y = self.y
        if self.name == "root":
            self.__nodes[0].x = 0
            self.__nodes[0].y = 0
            self.__nodes[0].__calculate_locations()
        elif self.name == "vertical":
            for i in range(len(self.__nodes)):
                self.__nodes[i].x=tmp_x
                self.__nodes[i].y=tmp_y
                self.__nodes[i].__calculate_locations()
                tmp_y += self.__nodes[i].height
        elif self.name == "horizontal":
            for i in range(len(self.__nodes)):
                self.__nodes[i].x=tmp_x
                self.__nodes[i].y=tmp_y
                self.__nodes[i].__calculate_locations()
                tmp_x += self.__nodes[i].width
        self.size_calculated = True

    def __calculate_sizes(self):
        if self.name == "root": #!!!!!!!!!!! NOT WORKING IF HEIGHT MORE THAN SCREEN
            if (float(self.__nodes[0].ratio[0]) / float(self.__nodes[0].ratio[1])) > self.width / self.height: # use width as equilizer
                print(self.width)
                self.__nodes[0].width = self.width
                self.__nodes[0].height = self.width * self.__nodes[0].ratio[1] / self.__nodes[0].ratio[0]
            else:   # use width as equilizer
                self.__nodes[0].height = self.height
                self.__nodes[0].width = self.height * self.__nodes[0].ratio[0] / self.__nodes[0].ratio[1]
            self.__nodes[0].__calculate_sizes()
        elif self.name == "vertical":
            for i in range(len(self.__nodes)):
                self.__nodes[i].width = self.width
                self.__nodes[i].height = self.width * self.__nodes[i].ratio[1] / self.__nodes[i].ratio[0]
                self.__nodes[i].__calculate_sizes()
        elif self.name == "horizontal":
            for i in range(len(self.__nodes)):
                self.__nodes[i].height = self.height
                self.__nodes[i].width = self.height * self.__nodes[i].ratio[0] / self.__nodes[i].ratio[1]
                self.__nodes[i].__calculate_sizes()

    def __calculate_real_ratios(self):
        self.size_calculated = False
        for i in range(len(self.__nodes)):
            self.__nodes[i].__calculate_real_ratios()

        if self.module != "":
            self.ratio = self.module.efky_getratio()
            self.non_rel_ratio = self.module.efky_getratio()

        if self.module == "":
            new_ratios = []

            # calculate new ratios
            for i in range(len(self.__nodes)):
                new_ratios.append( (self.__nodes[i].ratio[0], self.__nodes[i].ratio[1]) )

            for i in range(len(self.__nodes)):
                for j in range(len(self.__nodes)):
                    if i != j:
                        x = 1
                        if self.name == "vertical":
                            x = self.__nodes[i].ratio[0]  # * width for vertical
                        else:
                            x = self.__nodes[i].ratio[1]  # * height for horizontal
                        new_ratios[j] = (new_ratios[j][0] * x ,new_ratios[j][1] * x)

            # set objects ratios by new ratios
            for i in range(len(self.__nodes)):
                self.__nodes[i].ratio = new_ratios[i]

            # calculate containers ratio (root, horizontal and root have "0:0" ratio so
            # they must be calculated by their items
            r_w = 0
            r_h = 0
            if self.name == "vertical":
                r_w = self.__nodes[0].ratio[0] # widths are same for vertical
                for i in range(len(self.__nodes)):
                    r_h += self.__nodes[i].ratio[1]
            elif self.name == "horizontal":
                r_h = self.__nodes[0].ratio[1] # heights are same for horizontal
                for i in range(len(self.__nodes)):
                    r_w += self.__nodes[i].ratio[0]
	    elif self.name == "root":
                r_w = self.__nodes[0].ratio[0]
                r_h = self.__nodes[0].ratio[1]

            self.ratio = (r_w, r_h)
	    print(self.name + ": " +  str(r_w) + " - " + str(r_h))

    def draw_all(self, cr):
        EfkyHelper.messages.clear()
        if self.size_calculated:
            if self.module != "":
                n = self
                draw_helper = EfkyHelper(n.x, n.y, n.width, n.height, n.non_rel_ratio, cr)
                self.module.efky_draw(draw_helper)
            for i in range(len(self.__nodes)):
                self.__nodes[i].draw_all(cr)
        else:
            print("Error: Sizes must be calculated to draw!\nObj:" + self.name)


if __name__ == '__main__':
    sys.exit(main(sys.argv))











