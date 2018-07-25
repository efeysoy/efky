# -*- coding: utf-8 -*-
# https://query.yahooapis.com/v1/public/yql?q=select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='Istanbul')&format=json



# --==============================================================================
# --                            weather.py
# --
# --  Date    : 16.08.2016
# --  Author  : efeysoy
# --  Version : v0.1
# --  License : Distributed under the terms of GNU GPL version 2 or later
# --
# --==============================================================================
import subprocess

name = "memload"

x = 0

def efky_init():
    global name


def efky_getratio():
    return 1, 1


def efky_draw(dh):
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    p = subprocess.Popen([dir_path + '/mem_info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err != "":
        print("Error: " + err)

    lines = out.split('\n')

    mem_total = 0
    mem_used = 0
    for line in lines:
        vals = line.split('\t')
        if len(vals) <= 0:
            continue
        if vals[0] == "Memory Total:":
            mem_total = long(vals[1].split()[0])
        elif vals[0] == "Memory Locked:":
            mem_used = long(vals[1].split()[0])

    load = 0
    if mem_total != 0:
        load = 100 * float(mem_used) / mem_total

    dh.set_line_width(20)
    text = str(int(load))

    dh.draw_text(0.25 + (2 - len(text)) * 0.15, 0.40, 0.2, str(int(mem_used)), (1, 1, 1, 1))
    dh.draw_text(0.55, 0.30, 0.1, "MB", (1, 1, 1, 1))
    dh.draw_text(0.73, 0.31, 0.05, "Memory", (1, 1, 1, 1))
    dh.draw_text(0.73, 0.36, 0.05, "Load", (1, 1, 1, 1))

    if load < 50:
        color = (0, 1, 0, .2)
    elif load < 80:
        color = (.7, .7, 0, .2)
    else:
        color = (1, 0, 0, .2)

    dh.draw_arc(0.5, 0.5, 0.40, 0.5, (2 * 3.14 - 1) * (load / 100.0) + 0.5, color)
    dh.draw_arc(0.5, 0.5, 0.40, 0.5, 2 * 3.14 - 0.5, (1, 1, 1, .2))
