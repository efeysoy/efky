# --==============================================================================
# --                            efky_helper.py
# --
# --  Date    : 16.08.2016
# --  Author  : efeysoy
# --  Version : v0.1
# --  License : Distributed under the terms of GNU GPL version 2 or later
# --
# --==============================================================================

import cairo


class EfkyHelper:

    messages = {}

    def __init__(self, x, y, w, h, ratio, cr):
        self.ratio = ratio
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cr = cr
        self.cr.set_line_width(1)

    def set_line_width(self, width):
        self.cr.set_line_width(width)

    def fill_rectangle(self, x, y, w, h, color):
        self.cr.set_source_rgba(color[0], color[1], color[2], color[3])
        self.cr.rectangle(self.x + x * self.w, self.y + y * self.h,
                          w * self.w, h * self.h)
        self.cr.fill()

    def draw_rectangle(self, x, y, w, h, color):
        self.cr.set_source_rgba(color)
        self.cr.rectangle(self.x + x * self.w, self.y + y * self.h,
                          w * self.w, h * self.h)
        self.cr.stroke()

    def fill_arc(self, x, y, r, ang1, ang2, color):
        self.cr.set_source_rgba(color[0], color[1], color[2], color[3])
        self.cr.arc(self.x + x * self.w, self.y + y * self.h,
                          r * self.w, ang1, ang2)
        self.cr.fill()

    def draw_arc(self, x, y, r, ang1, ang2, color):
        self.cr.set_source_rgba(color[0], color[1], color[2], color[3])
        self.cr.arc(self.x + x * self.w, self.y + y * self.h,
                          r * self.w, ang1, ang2)
        self.cr.stroke()

    def draw_line(self, x, y, x2, y2, color):
        self.cr.set_source_rgba(color[0], color[1], color[2], color[3])
        self.cr.move_to(self.x + x * self.w, self.y + y * self.h)
        self.cr.rel_line_to(x2 * self.w,y2 * self.h)
        self.cr.stroke()

    def draw_text(self, x, y, size, text, color):
        self.cr.set_source_rgba(color[0], color[1], color[2], color[3])
        font_options = self.cr.get_font_options()
        ctm = self.cr.get_matrix()
        font_matrix = cairo.Matrix(size * self.h, 0, 0,size * self.h, 0, size * self.h)
        scaled_font = cairo.ScaledFont(self.cr.get_font_face(), font_matrix, ctm, font_options)

        self.cr.set_scaled_font(scaled_font)

        self.cr.move_to(self.x + x * self.w, self.y + y * self.h)

        self.cr.show_text(text)
        self.cr.stroke()

    def draw_centered_text(self, x, y, size, text, color):
        self.cr.set_source_rgba(color[0], color[1], color[2], color[3])
        font_options = self.cr.get_font_options()
        ctm = self.cr.get_matrix()
        font_matrix = cairo.Matrix(size * self.h, 0, 0,size * self.h, 0, size * self.h)
        scaled_font = cairo.ScaledFont(self.cr.get_font_face(), font_matrix, ctm, font_options)

        self.cr.set_scaled_font(scaled_font)

        (xt, yt, widtht, heightt, dxt, dyt) = self.cr.text_extents(text)

        self.cr.move_to(self.x + x * self.w - widtht / 2, self.y + y * self.h)

        self.cr.show_text(text)
        self.cr.stroke()

    def set_font(self, font_name, arg1, arg2):
        self.cr.select_font_face(font_name, arg1, arg2)

    def draw_image(self, x, y,width, height, url):
        import gtk
        # import subprocess
        # p = subprocess.Popen(['convert', '-verbose', '32.gif', '32.png'], stdout=subprocess.PIPE,
        #                      stderr=subprocess.PIPE)
        # out, err = p.communicate()
        # if err != "":
        #     print("Error: " + err)
        img = gtk.image_new_from_file(url)
        # from pprint import pprint
        # pprint(img)
        # surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, img.get_pixbuf().get_width(), img.get_pixbuf().get_height())
        # ctx = cairo.Context(surf)
        # gdkcr = gtk.gdk.CairoContext(ctx)
        # gdkcr.set_source_pixbuf(img.get_pixbuf(), 0, 0)
        pixbuf = img.get_pixbuf().scale_simple(int(width * self.w), int(height * self.h), gtk.gdk.INTERP_BILINEAR)
        self.cr.set_source_pixbuf(pixbuf, self.x + x * self.w, self.y + y * self.w)
        self.cr.paint()

# def dump(obj):
#   for attr in dir(obj):
#     print "obj.%s = %s" % (attr, getattr(obj, attr))
