#!/usr/bin/python

import httplib
import json
import re
import curses


scr = curses.initscr()
curses.noecho()
curses.cbreak()

def load(page):

    conn = httplib.HTTPConnection("teletekst-data.nos.nl")
    conn.request("GET", "/json/" + str(page))
    r = conn.getresponse()
    data = {}

    if r.status == 200:
        data = json.loads(r.read())

    conn.close()
    return data

def fix_chars(l):
    l = re.sub("&#x....;", ' ', l)
    return l

def fix_attr(s):
    return ""

def show_line(l, y):
    l = re.sub('<[^<]+?>', '', l)
    l = fix_chars(l)
    scr.addstr(y, 0, l)


def show(page):
    p = load(page)
    ls = p['content'].split('\n')
    y = 1
    for l in ls:
        show_line(l, y)
        y = y + 1

show(101)

while True:
    c = scr.getch()
    if c == ord('q'):
        break

curses.endwin()

# vi: ft=python
