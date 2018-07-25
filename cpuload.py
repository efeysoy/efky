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

name = "cpuload"

cpu_total = 0
cpu_idle = 0
x = 0

def efky_init():
    global name


def efky_getratio():
    return 1, 1


def efky_draw(dh):
    global cpu_total
    global cpu_idle
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    p = subprocess.Popen([dir_path + '/cpu_info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err != "":
        print("Error: " + err)

    lines = out.split('\n')

    cpu_total_new = 0
    cpu_idle_new = 0
    for line in lines:
        vals = line.split('\t')
        if len(vals) <= 0:
            continue
        if vals[0] == "Cpu Total:":
            cpu_total_new = long(vals[1])
        elif vals[0] == "Cpu Idle:":
            cpu_idle_new = long(vals[1])

    load = 0
    if cpu_total == 0:
        cpu_total = cpu_total_new
        cpu_idle = cpu_idle_new
    else:
        total = (cpu_total_new - cpu_total)
        idle = (cpu_idle_new - cpu_idle)
        load = 100 * float(total - idle) / total
        cpu_total = cpu_total_new
        cpu_idle = cpu_idle_new

    dh.set_line_width(20)
    text = str(int(load))
    dh.draw_arc(0.5, 0.5, 0.40, 0.5, 2 * 3.14 - 0.5, (1, 1, 1, .2))
    dh.draw_text(0.20 + (2 - len(text)) * 0.15, 0.30, 0.3, str(int(load)), (1, 1, 1, 1))
    dh.draw_text(0.57, 0.30, 0.15, "%", (1, 1, 1, 1))
    dh.draw_text(0.73, 0.33, 0.05, "CPU", (1, 1, 1, 1))
    dh.draw_text(0.73, 0.38, 0.05, "Load", (1, 1, 1, 1))
    if load < 50:
        color = (0, 1, 0, .2)
    elif load < 80:
        color = (.7, .7, 0, .2)
    else:
        color = (1, 0, 0, .2)
    dh.draw_arc(0.5, 0.5, 0.40, 0.5, (2 * 3.14 - 1) * (load / 100.0) + 0.5, color)

