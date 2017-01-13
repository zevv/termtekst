#!/usr/bin/python

import os
import sys

from lxml import html
import json

TELETEKST = "http://teletekst-data.nos.nl/json/%i"

error = ['Unable to import... \n %s\n',
        '']

warn = ['Defaulting to page 100 \n',
        '']

def main():
    '''
    >>> main()
    http://teletekst-data.nos.nl/json/100
    '''

    try:
        import ncurses
    except ImportError as e:
        msg = error[0] % str(e)
        sys.stderr.write(msg)
        sys.exit(-1)
        pass

    try:
        import requests
    except ImportError as e:
        msg = error[0] % str(e)
        sys.stderr.write(msg)
        sys.exit(-1)
        pass

    page = 100
    try:
        if int(sys.argv[1]) and int(sys.argv[1]) < 999:
            page = int(sys.argv[1])
    except:
        msg = warn[0] + '\n'
        sys.stdout.write(msg)

    page = TELETEKST % page
    print(page)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        import doctest
        doctest.testmod()
    else:
        main()
