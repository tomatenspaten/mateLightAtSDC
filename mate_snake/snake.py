#!/usr/local/bin/python3
from collections import deque
from random import randint
from tkinter import Tk, Canvas, Frame, BOTH
import opcmapper
import opc

numLEDs = 255
client = opc.Client('localhost:7890')

pixels = [(0, 0, 0)] * numLEDs
client.put_pixels(pixels)

X, Y = (15, 12)
BLOCK_SIZE = 10

layout = './layouts/sdc.json'

KEY_LEFT = 'Left'
KEY_RIGHT = 'Right'
KEY_UP = 'Up'
KEY_DOWN = 'Down'
KEY_QUIT = 'q'

LEVEL_THRESHOLD = 2
SNAKE_COLOR = '#00f'
FOOD_COLOR = '#f00'

VALID_DIRECTIONS = {
    KEY_LEFT: set((KEY_LEFT, KEY_UP, KEY_DOWN)),
    KEY_RIGHT: set((KEY_RIGHT, KEY_UP, KEY_DOWN)),
    KEY_UP: set((KEY_UP, KEY_LEFT, KEY_RIGHT)),
    KEY_DOWN: set((KEY_DOWN, KEY_LEFT, KEY_RIGHT))
}

MOVEMENTS = {
    KEY_LEFT: lambda x, y: (x - 1, y),
    KEY_RIGHT: lambda x, y: (x + 1, y),
    KEY_UP: lambda x, y: (x, y - 1),
    KEY_DOWN: lambda x, y: (x, y + 1)
}

opcmapper.parse_layout(layout)
window = Tk()
window.geometry('{}x{}'.format(X * BLOCK_SIZE, Y * BLOCK_SIZE))
window.resizable(False, False)

frame = Frame(window)
frame.master.title('Snake')
frame.pack(fill=BOTH, expand=1)

canvas = Canvas(frame)
canvas.pack(fill=BOTH, expand=1)


def frame_off():
    global pixels
    pixels = [(0, 0, 0)] * numLEDs
    client.put_pixels(pixels)


def add_to_current_pixel_frame(x, y, color):
    #print('x:', x)
    #print('y:', y)
    pixels[opcmapper.find_led_number_for_x_and_y_value(x, y)] = color


def create_game():
    return {
        'snake': deque(((5, 5), (5, 6))),
        'food': (0, 0),
        'direction': KEY_RIGHT,
        'moves': deque(),
        'points': 0,
        'speed': 1
    }


game = create_game()


def draw_rect(x, y, color=SNAKE_COLOR):
    x1 = x * BLOCK_SIZE
    y1 = y * BLOCK_SIZE
    x2 = x1 + BLOCK_SIZE
    y2 = y1 + BLOCK_SIZE
    return canvas.create_rectangle(x1, y1, x2, y2, outline='', fill=color)


def render():
    # this could be optimized by moving the tail to the head, or just appending
    # the head when the snake eats
    canvas.delete('all')
    frame_off()

    for x, y in game['snake']:
        draw_rect(x, y)
        color=(0,0,255)
        add_to_current_pixel_frame(x, y, color)
    x, y = game['food']
    draw_rect(x, y, color=FOOD_COLOR)
    color=(255,0,0)
    add_to_current_pixel_frame(x, y,color)
    client.put_pixels(pixels)


def gen_food(snake):
    while True:
        food = randint(0, X - 1), randint(0, Y - 1)
        if food not in snake:
            return food


def eat(snake):
    game['food'] = gen_food(snake)
    game['points'] += 1
    if not game['points'] % LEVEL_THRESHOLD:
        game['speed'] += 1
    print('points: {}, speed: {}'.format(game['points'], game['speed']))


def move_snake(direction):
    snake = set(game['snake'])
    u, w = game['snake'][-1]
    next_point = MOVEMENTS[direction](u, w)

    if next_point == game['food']:
        eat(snake)
    else:
        game['snake'].popleft()

    x, y = next_point

    if x < 0 or x >= X or y < 0 or y >= Y:
        raise ValueError('You crashed into a wall!')

    if next_point in snake:
        raise ValueError('You just ate yourself!')

    game['snake'].append(next_point)


def handle_next_movement():
    direction = game['moves'].popleft() if game['moves'] else game['direction']
    game['direction'] = direction
    move_snake(direction)


def on_press(event):
    key = event.keysym

    prev_direction = game['moves'][-1] if game['moves'] else game['direction']
    if key in VALID_DIRECTIONS[prev_direction]:
        game['moves'].append(key)
    elif key == KEY_QUIT:
        window.destroy()


def tick():
    handle_next_movement()
    render()
    window.after(int(1000 / game['speed']), tick)


def main():
    window.bind('<Key>', on_press)
    tick()
    window.mainloop()


if __name__ == '__main__':
    main()
