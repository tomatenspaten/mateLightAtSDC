#!/usr/bin/env python3

import time

import opc
import opcmapper
import character

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


max_width = 15
x_offset = max_width
opcmapper.parse_layout(layout)
char = character.Character(char_c, max_width)

while True:
    pixels = [(0, 0, 0)] * numLEDs
    client.put_pixels(pixels)

    for pixel in char.get_coordinates():
        pixels[opcmapper.find_led_number_for_x_and_y_value(pixel[0], pixel[1])] = (0, 255, 0)
    client.put_pixels(pixels)
    time.sleep(0.4)
    char.rotate()
