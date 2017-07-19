# --==============================================================================
# --                            weekpercent.py
# --
# --  Date    : 16.08.2016
# --  Author  : efeysoy
# --  Version : v0.1
# --  License : Distributed under the terms of GNU GPL version 2 or later
# --
# --==============================================================================
import datetime

name = "weekpercent"

start_day = 0    # Monday
end_day = 4      # Friday
start_hour = 8
end_hour = 17

def efky_init():
    global name


def efky_getratio():
    return 5, 2


def efky_draw(dh):
    day = datetime.datetime.today().weekday()
    hour = datetime.datetime.today().hour
    dh.fill_rectangle(0, 0, 1, 1, (0, 0, 0, .2))
    daypercent = ((day - start_day) / float(end_day - start_day + 1)) * 100
    hourtotalpercent = 100 / float(end_day - start_day + 1)
    hourpercent = ((hour - start_hour) / float(end_hour - start_hour)) * hourtotalpercent
    hourpercent = 100 if hourpercent > 100 else hourpercent
    hourpercent = 0 if hourpercent < 0 else hourpercent
    totalpercent = (hourpercent + daypercent) / 100
    dh.set_line_width(20)
    dh.draw_line(0.1, 0.3, 0.8, 0, (1, 1, 1, .5))
    dh.draw_line(0.1, 0.3, totalpercent * 0.8, 0, (1, 0, 0, .5))
    dh.draw_centered_text(0.5, 0.4, 0.5, str(int(totalpercent*100))+"%", (1, 1, 1, .5))
    # print day
    # print hour
    # print daypercent
    # print hourpercent
    # print totalpercent





