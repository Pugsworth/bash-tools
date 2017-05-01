#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

color_fg_prefix = '\033[38;5;'
color_bg_prefix = '\033[48;5;'

def co_system_colors():
    color_order = [
         0, 1,  2,  3,  4,  5,  6,  7,
        -1,
         8, 9, 10, 11, 12, 13, 14, 15
    ]
    for i in color_order:
        if (i == -1):
            print("%s%im" % (color_fg_prefix, 0))
        else:
            print("%s%im %0.2i " % (color_bg_prefix, i, i), end='')

    print("\033[0m\n")

def co_extended_colors():
    for i in range(16, 232):
        # the last 4 rows per slice is a little hard to read
        if ((math.floor((i-4)/6.0) % 6) in (0, 1, 4, 5)):
            print("%s%im" % (color_fg_prefix, 0), end='')
        else:
            print("%s%im" % (color_fg_prefix, 15), end='')

        print("%s%im %03i %s" % (color_bg_prefix, i, i, ''), end='')
        if ((i-3) % 6 == 0):
            print()

    print("\033[0m\n")

def co_grayscale_colors():
    for i in range(232, 256):
        if i>232 and i % 8 == 0:
            print()
        print("%s%im %03i " % (color_bg_prefix, i, i), end='')

    print("\033[0m\n")


co_system_colors()
co_extended_colors()
co_grayscale_colors()

