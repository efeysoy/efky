# --==============================================================================
# --                            upspeed.py
# --
# --  Date    : 16.08.2016
# --  Author  : efeysoy
# --  Version : v0.1
# --  License : Distributed under the terms of GNU GPL version 2 or later
# --
# --==============================================================================

name = "downspeed"
#dev = "wlx7cdd90821717"
dev = "enp0s31f6"
# dev = "wlp1s0"

prev = 0
val = [0, 0, 0, 0, 0]
graph = [0] * 50

def efky_init():
    global name


def efky_getratio():
    return 5, 3


def efky_draw(dh):
    global val
    global prev
    rt = efky_getratio()

    file = open("/sys/class/net/" + dev + "/statistics/tx_bytes")
    if prev == 0:
        prev = int(file.read().strip())
        result = 0
    else:
        curr = int(file.read().strip())
        result = curr - prev
        prev = curr
    val.append((result + val[-1]) / 2)
    val.pop(0)
    file.close()

    result = sum(val) / float(len(val))
    lbl = result
    unit = "B/s"
    if lbl > 1024:
        lbl /= 1024
        unit = "KB/s"
    if lbl > 1024:
        lbl /= 1024
        unit = "MB/s"   
    graph.append(result)
    graph.pop(0)
    mx = max(graph)

    dh.draw_text(0.05, 0.1, 0.15, "Upload", (1, 1, 1, 1))
    dh.draw_text(0.05, 0.5, 0.30, str(round(lbl, 2)) + " " + unit, (1, 1, 1, .5))
    for i in range(len(graph)):
        if mx == 0:
            pr = 0
        else:
            pr = - graph[i] / float(mx)
            dh.draw_line(i * 0.02, 1, 0, pr, (1, .7, .1, .5))









