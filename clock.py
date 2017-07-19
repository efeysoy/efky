# --==============================================================================
# --                            clock.py
# --
# --  Date    : 16.08.2016
# --  Author  : efeysoy
# --  Version : v0.1
# --  License : Distributed under the terms of GNU GPL version 2 or later
# --
# --==============================================================================

import datetime
from math import sin, cos, pi


def efky_getratio():
    return 1, 1


def efky_draw(dh):
    current_time = datetime.datetime.now().time()
    hour = current_time.hour
    minu = current_time.minute
    sec = current_time.second
    # Draw a fancy little circle for demonstration purpose
    dh.fill_arc(0.5, 0.5, 0.5, 0, 3.14 * 2, (1, 1, 1, 0.25))

    dh.draw_text(0.15, 0.35, 0.3, str(hour) if len(str(hour)) > 1 else "0" + str(hour), (0.1, 0.1, 0.1, 0.5))
    dh.draw_text(0.55, 0.45, 0.2, str(minu) if len(str(minu)) > 1 else "0" + str(minu), (0.1, 0.1, 0.1, 0.5))

    lln1 = 0.45
    lln2 = 0.30

    hour %= 12
    degH = 2*pi * hour / 12 - pi/2
    degM = 2*pi * minu / 60 - pi/2
    degS = 2 * pi * sec / 60 - pi / 2

    dh.cr.set_line_width(2)
    dh.draw_line(0.5, 0.5, cos(degM) * lln1, sin(degM) * lln1, (0.0, 0.0, 0.0, 1))

    
    dh.draw_line(0.5, 0.5, cos(degH) * lln2, sin(degH) * lln2, (0.5, 0.0, 0.0, 1))

    dh.cr.set_line_width(0.5)
    dh.draw_line(0.5, 0.5, cos(degS) * lln1, sin(degS) * lln1, (1, 1, 1, 1))
    dh.cr.set_line_width(1)

