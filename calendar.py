# --==============================================================================
# --                            calendar.py
# --
# --  Date    : 16.08.2016
# --  Author  : efeysoy
# --  Version : v0.1
# --  License : Distributed under the terms of GNU GPL version 2 or later
# --
# --==============================================================================

import subprocess
import datetime
import cairo


def efky_getratio():
    return (4,3)


def efky_draw(dh):
    p = subprocess.Popen(['cal', '-m', '--color=never'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err != "":
        print("Error: " + err)
    day = datetime.datetime.now().day

    x = 0.15
    y = 0.10
    lines = out.split("\n")
    dh.set_font("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    dh.draw_text(x, y, 0.10, lines[0].strip(), (0.6, 0.6, 0.6, 1))
    dh.set_font("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

    y += 0.1
    for i in range(1, len(lines)):
        if lines[i].strip() == "":
            continue
        chars = lines[i].strip().split()
        space = 0
        if chars[0] == "1" and len(chars) < 7:
            space = 0.11 * (7 - len(chars))
        for j in range(len(chars)):
            if str(day) == chars[j]:
                dh.draw_text(x + j * 0.11 + space, y + i * 0.1, 0.06, chars[j], (.8, 1, .8, 1))
            else:
                dh.draw_text(x + j * 0.11 + space, y + i * 0.1, 0.06, chars[j], (0.6, 0.6, 0.6, 1))

