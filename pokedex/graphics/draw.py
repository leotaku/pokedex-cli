# -*- coding: utf-8 -*-

import os
import textwrap
from PIL import Image

from .. import resource_path
from .colors import rgb_to_xterm
from .conversion import rgb2short


block_top = "▀"
numbers = {
    "0": [u"┌─┐",
          u"│ │",
          u"└─┘"],
    "1": [u" ┐ ",
          u" │ ",
          u" ┴ "],
    "2": [u"┌─┐",
          u"┌─┘",
          u"└─┘"],
    "3": [u"┌─┐",
          u" ─┤",
          u"└─┘"],
    "4": [u"┬ ┬",
          u"└─┤",
          u"  ┴"],
    "5": [u"┌─┐",
          u"└─┐",
          u"└─┘"],
    "6": [u"┌─┐",
          u"├─┐",
          u"└─┘"],
    "7": [u"┌─┐",
          u"  │",
          u"  ┴"],
    "8": [u"┌─┐",
          u"├─┤",
          u"└─┘"],
    "9": [u"┌─┐",
          u"└─┤",
          u"└─┘"],
    "#": [u" ┼┼",
          u" ┼┼",
          u"   "],
}

type_colors = {
    "normal":   int(rgb2short("A8A77A")[0]),
    "fire":     int(rgb2short("EE8130")[0]),
    "water":    int(rgb2short("6390F0")[0]),
    "electric": int(rgb2short("F7D02C")[0]),
    "grass":    int(rgb2short("7AC74C")[0]),
    "ice":      int(rgb2short("96D9D6")[0]),
    "fighting": int(rgb2short("C22E28")[0]),
    "poison":   int(rgb2short("A33EA1")[0]),
    "ground":   int(rgb2short("E2BF65")[0]),
    "flying":   int(rgb2short("A98FF3")[0]),
    "psychic":  int(rgb2short("F95587")[0]),
    "bug":      int(rgb2short("A6B91A")[0]),
    "rock":     int(rgb2short("B6A136")[0]),
    "ghost":    int(rgb2short("735797")[0]),
    "dragon":   int(rgb2short("6F35FC")[0]),
    "dark":     int(rgb2short("705746")[0]),
    "steel":    int(rgb2short("B7B7CE")[0]),
    "fairy":    int(rgb2short("D685AD")[0]),
}


def draw_image(buffer, path, x0=0, y0=0):
    image = Image.open(path).convert("RGB")
    pixels = image.load()
    width, height = image.size

    for y in range(0, height, 2):
        for x in range(width):
            if x + x0 < buffer.width and y + y0 < buffer.height * 2:
                color_top = rgb_to_xterm(pixels[x, y])
                color_bottom = rgb_to_xterm(pixels[x, y + 1])

                buffer.put_cell((x0 + x, (y0 + y) // 2), u"▀", color_top, color_bottom)


def draw_number(buffer, number, x0=0, y0=0, fg=15, bg=-1):
    chars = "#%03d" % number
    for i, char in enumerate(chars):
        template = numbers[char]
        for x in range(3):
            for y in range(3):
                buffer.put_cell((x0 + (i*3) + x, y0 + y), template[y][x], fg, bg)


def draw_type(buffer, type1, type2=None, x0=0, y0=0):
    buffer.put_line((x0, y0), " %s " % type1.upper(), fg=0, bg=type_colors[type1.lower()])
    if type2:
        buffer.put_line((x0 + len(type1) + 3, y0), " %s " % type2.upper(), fg=0, bg=type_colors[type2.lower()])


def draw_flavor_text(buffer, text, width, x0=0, y0=0, fg=15, bg=-1):
    # Non-asian languages only!
    lines = textwrap.fill(text, width=width).split("\n")
    for i, line in enumerate(lines):
        buffer.put_line((x0, y0 + i), line, fg, bg)


def draw_evolutions(buffer, chain, index, x0=0, y0=0, bg=-1):
    offset = 0
    for i, stage in enumerate(chain):
        fg = 245 if i != index else 15
        buffer.put_line((x0 + offset, y0), ("#%03d" % stage[0]).center(len(stage[1])), fg, bg)
        buffer.put_line((x0 + offset, y0 + 1), stage[1], fg, bg)
        offset += len(stage[1])
        if i < len(chain) - 1:
            buffer.put_line((x0 + offset, y0 + 1), " > ", 33, bg)
            offset += 3
