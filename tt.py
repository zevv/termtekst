#!/usr/bin/python
# -*- coding: UTF-8 -*-

import httplib
import json
import sys
import re
import curses
import locale
from datetime import datetime
from HTMLParser import HTMLParser

tt_re = re.compile(u'([\U0000f020-\U0000f100])')
locale.setlocale(locale.LC_ALL, '')

html = HTMLParser()

# Map teletext graphics (2x3) to braille (2x4)
#
#  01 02      01 08
#  04 08 ==>  02 10
#  10 20      04 20
#             40 80

tt_to_br = {
    0x01: 0x01, 0x02: 0x08, 0x04: 0x06,
    0x08: 0x30, 0x10: 0x40, 0x20: 0x80,
}

colors_fg = {
    'red': 1,
    'green': 2,
    'yellow': 3,
    'blue': 4,
    'magenta': 5,
    'cyan': 6,
    'white': 7,
}

colors_bg = {
    'bg-red': 1,
    'bg-green': 2,
    'bg-yellow': 3,
    'bg-blue': 4,
    'bg-magenta': 5,
    'bg-cyan': 6,
    'bg-white': 7,
}


def load(page):
    conn = httplib.HTTPConnection("teletekst-data.nos.nl")
    conn.request("GET", "/json/" + str(page))
    r = conn.getresponse()
    data = {}

    if r.status == 200:
        data = json.loads(r.read())

    conn.close()
    return data


def braille_graph(c):
    n = ord(c.group(1)) - 0xf020
    if n >= 64:
        n = n - 32
    m = 0
    for v in tt_to_br:
        if n & v:
            m = m | tt_to_br[v]
    return unichr(0x2800 + m)


def fix_chars(l):
    l = html.unescape(l)
    l = tt_re.sub(braille_graph, l)
    return l.encode('utf-8')


def show_line(scr, l):

    class Parser(HTMLParser):

        def __init__(self):
            HTMLParser.__init__(self)
            self.bg = 0

        def handle_starttag(self, tag, attrs):
            self.fg = 7
            for attr in attrs:
                if attr[0] == "class":
                    for c in re.finditer("(\S+)", attr[1]):
                        c = c.group(1)
                        if c in colors_fg:
                            self.fg = colors_fg[c]
                        if c in colors_bg:
                            self.bg = colors_bg[c]

            attr = 0
            if self.bg > 0:
                attr = curses.color_pair(self.fg*8 + self.bg) + curses.A_REVERSE
            else:
                attr = curses.color_pair(self.bg*8 + self.fg)

            scr.attrset(attr + curses.A_BOLD)

        def handle_endtag(self, tag):
            pass

        def handle_data(self, data):
            scr.addstr(data)

    scr.attrset(0)
    parser = Parser()
    parser.feed(l)


def show(scr, p):
    scr.erase()
    if 'content' in p:
        ls = p['content'].split('\n')
        y = 0
        for l in ls:
            scr.attrset(0)
            scr.addstr(0, 3, datetime.now().strftime('%H:%M:%S'))
            try:
                scr.move(y, 0)
                show_line(scr, fix_chars(l))
            except:
                pass
            y = y + 1
        return p


def main(scr):

    curses.noecho()
    curses.cbreak()
    curses.halfdelay(1)
    curses.start_color()
    curses.curs_set(0)

    page = '100'
    page_user = ''
    page_next = ''
    ticks_idle = 0

    if len(sys.argv) > 1:
        page = sys.argv[1]

    for i in range(1, 64):
        curses.init_pair(i, (i % 8), i/8)

    p = load(page)

    while True:

        show(scr, p)

        if len(page_user) > 0:
            scr.addstr(0, 36, page_user + '   ')

        c = scr.getch()

        if c == -1:
            ticks_idle = ticks_idle + 1
            if ticks_idle == 5:
                page_user = ''
        else:
            ticks_idle = 0

        if c == ord('q'):
            break
        if c == curses.KEY_DOWN or c == ord('j') or c == ord(','):
            page_next = p['prevSubPage']
        if c == curses.KEY_UP or c == ord('k') or c == ord('.'):
            page_next = p['nextSubPage']
        if c == curses.KEY_LEFT or c == ord('h') or c == ord('['):
            page_next = p['prevPage']
        if c == curses.KEY_RIGHT or c == ord('l') or c == ord(']'):
            page_next = p['nextPage']
        if c >= ord('0') and c <= ord('9'):
            page_user = page_user + chr(c)
            if len(page_user) == 3:
                page_next = page_user
                page_user = ''

        if page_next and len(page_next) > 0:
            page = page_next
            page_next = None
            scr.addstr(9,  12, "               ")
            scr.addstr(10, 12, "    Loading    ")
            scr.addstr(11, 12, "               ")
            scr.refresh()
            p = load(page)


curses.wrapper(main)

# vi: ft=python
