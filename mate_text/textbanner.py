#!/usr/bin/env python3

import time

import opc
import opcmapper

char_c = [
    ['.', 'x', 'x', 'x', 'x', 'x'],
    ['x', 'x', 'x', 'x', 'x', 'x'],
    ['x', 'x', '.', '.', '.', '.'],
    ['x', 'x', '.', '.', '.', '.'],
    ['x', 'x', '.', '.', '.', '.'],
    ['x', 'x', '.', '.', '.', '.'],
    ['x', 'x', '.', '.', '.', '.'],
    ['x', 'x', '.', '.', '.', '.'],
    ['x', 'x', '.', '.', '.', '.'],
    ['x', 'x', '.', '.', '.', '.'],
    ['x', 'x', 'x', 'x', 'x', 'x'],
    ['.', 'x', 'x', 'x', 'x', 'x']
]

# char_c = [
#     ['.', 'x', 'x', 'x', 'x'],
#     ['x', '.', '.', '.', '.'],
#     ['x', '.', '.', '.', '.'],
#     ['x', '.', '.', '.', '.'],
#     ['.', 'x', 'x', 'x', 'x']
# ]

numLEDs = 255
client = opc.Client('localhost:7890')
layout = './layout/sdc.json'

pixels = [(0, 0, 0)] * numLEDs
client.put_pixels(pixels)


def get_coordinates(c, x_offset):
    chars = []
    for y, row in enumerate(c):
        for x, col in enumerate(row):
            if col == 'x':
                chars.append((x + x_offset, y))
    return chars


# ----------------
def rotate(buffer):
    return buffer[1:] + buffer[:1]


max_width = 14
x_offset = max_width
opcmapper.parse_layout(layout)
while True:
    pixels = [(0, 0, 0)] * numLEDs
    client.put_pixels(pixels)
    whole_char = get_coordinates(char_c, x_offset)
    whole_char = [x for x in whole_char if 0 <= x[0] <= max_width]
    print('====================')
    print(whole_char)
    print('====================')

    for pixel in whole_char:
        pixels[opcmapper.find_led_number_for_x_and_y_value(pixel[0], pixel[1])] = (0, 255, 0)
    client.put_pixels(pixels)
    x_offset = x_offset - 1 if len(whole_char) > 2 else max_width
    time.sleep(0.4)
