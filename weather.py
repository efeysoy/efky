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
import urllib2
import json
import cairo
import subprocess
from pprint import pprint

name = "weather"
location = "Istanbul"

counter = 0
data = None

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
    return 3, 2


def efky_draw(dh):
    global counter
    global data
    global http, https, proxy_mode
    dh.fill_rectangle(0, 0, 1, 1, (1, 1, 1, .2))
    if counter == 0:
        counter += 1
        if proxy_mode == "'manual'":
            proxy_support = urllib2.ProxyHandler({"https": https, "http": http})
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)
        url = "https://query.yahooapis.com/v1/public/yql?q=select * from weather.forecast where woeid in " + \
              "(select woeid from geo.places(1) where text='Istanbul') and u='C'&format=json"
        url = url.replace(" ", "%20")
        try:
            jsn = urllib2.urlopen(url).read()
        except URLError:
            return
        data = json.loads(jsn)
        data = data["query"]["results"]["channel"]
        desc = data["item"]["description"]

        str = desc.find('<img src="') + 10
        end = desc.find('"/>', str)
        link = desc[str:end]

        if proxy_mode == "'manual'":
            urllib2.install_opener(opener)
        iconfile = urllib2.urlopen(link)
        with open('/tmp/32.gif', 'wb') as output:  # async?!?!?!
            output.write(iconfile.read())

    else:
        counter = (counter + 1) % 600
    if data is not None:
        tmp = "°" + data["units"]["temperature"]
        loc = data["location"]["city"] + "," + data["location"]["country"]
        now = data["item"]["condition"]["temp"] + tmp
        frcst = data["item"]["forecast"]

        dh.set_font("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

        dh.draw_image(0.05, 0.05, 0.3, 0.45, "/tmp/32.gif")
        dh.draw_text(0.40, 0.07, 0.1, loc, (0, 0, 0, .8))
        dh.draw_text(0.40, 0.15, 0.3, now, (.8, .8, .8, 1))

        for i in range(1,4):
            dh.draw_centered_text(0.2 + (i - 1) * 0.3, 0.55, 0.1, frcst[i]["date"][:-4], (.8, .8, .8, 1))
            dh.set_font("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            dh.draw_centered_text(0.2 + (i - 1) * 0.3, 0.70, 0.07, frcst[i]["high"] + "|" + frcst[i]["low"] + tmp, (.9, .9, .9, 1))
            dh.set_font("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

            frcst_lines = frcst[i]["text"].split()
            for j in range(len(frcst_lines)):
                dh.draw_centered_text(0.2 + (i - 1) * 0.3, 0.80 + (j * 0.065), 0.06, frcst_lines[j], (1, 1, 1, 1))






