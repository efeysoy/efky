# -*- coding: utf-8 -*-
# http://download.finance.yahoo.com/d/quotes.csv?s=EURTRY=X&f=sl1d1t1ba&e=.xml



# --==============================================================================
# --                            weather.py
# --
# --  Date    : 16.08.2016
# --  Author  : efeysoy
# --  Version : v0.1
# --  License : Distributed under the terms of GNU GPL version 2 or later
# --
# --==============================================================================
import urllib2
import cairo
import subprocess
import datetime
from pprint import pprint

name = "currexchange"

curr_from = "TRY"
currs = {"EUR", "USD", "GBP"}

counter = 0
data = None
vals = None
title = ""

proxy_mode = "'none'"
http = ""
https = ""


def efky_init():
    global http, https, proxy_mode
    p = subprocess.Popen(['gsettings', 'get', 'org.gnome.system.proxy', 'mode'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err != "":
        print("Error: " + err)

    print("Proxy mode: " + out)

    if out.strip() == "'manual'":
        proxy_mode = out.strip()
        p = subprocess.Popen(['gsettings', 'get', 'org.gnome.system.proxy.http', 'host'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err != "":
            print("Error: " + err)
        http = out.replace("'", "")
        p = subprocess.Popen(['gsettings', 'get', 'org.gnome.system.proxy.http', 'port'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err != "":
            print("Error: " + err)
        http = http.strip() + ":" + out.strip()

        p = subprocess.Popen(['gsettings', 'get', 'org.gnome.system.proxy.https', 'host'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err != "":
            print("Error: " + err)
        https = out.replace("'", "")
        p = subprocess.Popen(['gsettings', 'get', 'org.gnome.system.proxy.https', 'port'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err != "":
            print("Error: " + err)
        https = https.strip() + ":" + out.strip()
    print("HTTP: " + http)
    print("HTTPS: " + https)
    global name


def efky_getratio():
    return 2, 1


def efky_draw(dh):
    global counter
    global data
    global http, https, proxy_mode
    global vals
    global title
    dh.fill_rectangle(0, 0, 1, 1, (1, 1, 1, .2))
    if counter == 0:
        counter += 1
        vals = dict()
        title = datetime.datetime.today().strftime("Kur: %d.%m.%y %H:%M")
        for curr in currs:
            if proxy_mode == "'manual'":
                proxy_support = urllib2.ProxyHandler({"https": https, "http": http})
                opener = urllib2.build_opener(proxy_support)
                urllib2.install_opener(opener)
            url = "http://download.finance.yahoo.com/d/quotes.csv?s="+ curr + curr_from + "=X&f=sl1d1t1ba&e=.csv"
            url = url.replace(" ", "%20")
            try:
                data = urllib2.urlopen(url).read()
            except URLError:
                return
            data = data.split(",")
            vals[curr] = data[1]
            pprint(vals)
    else:
        counter = (counter + 1) % 600
    if vals is not None:
        # items = vals.items()
        # for i in range(len(items)):
        #     # dh.set_font("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        #     dh.draw_centered_text(0.5, 0.075, 0.2, title, (1, 1, 1, .5))
        #     dh.draw_text(0.20, 0.35 + i * 0.20, 0.15, "1 " + items[i][0] + " = " + items[i][1] + " " + curr_from, (0, 0, 0, .5))
        i = 0
        for curr in currs:
            # dh.set_font("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            dh.draw_centered_text(0.5, 0.075, 0.2, title, (1, 1, 1, .5))
            dh.draw_text(0.20, 0.35 + i * 0.20, 0.15, "1 " + curr + " = " + vals[curr] + " " + curr_from, (0, 0, 0, .5))
            i += 1

        # dh.draw_text(0.40, 0.15, 0.3, now, (.8, .8, .8, 1))
        #
        # for i in range(1,4):
        #     dh.draw_centered_text(0.2 + (i - 1) * 0.3, 0.55, 0.1, frcst[i]["date"][:-4], (.8, .8, .8, 1))
        #     dh.set_font("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        #     dh.draw_centered_text(0.2 + (i - 1) * 0.3, 0.70, 0.07, frcst[i]["high"] + "|" + frcst[i]["low"] + tmp, (.9, .9, .9, 1))
        #     dh.set_font("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        #
        #     frcst_lines = frcst[i]["text"].split()
        #     for j in range(len(frcst_lines)):
        #         dh.draw_centered_text(0.2 + (i - 1) * 0.3, 0.80 + (j * 0.065), 0.06, frcst_lines[j], (1, 1, 1, 1))






