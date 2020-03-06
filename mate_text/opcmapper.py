import json

default_layout = './layout/sdc.json'

coordinates = []
transform_factor = 10  # necessary due to strange scaling in json layout: 0.1, 0,2,...
z = 0.00  # no z-values in 2d mate matrix
correction_to_zero_based_scale = 1


def parse_layout(layout):
    for item in json.load(open(layout)):
        if 'point' in item:
            coordinates.append(tuple(item['point']))


def find_led_number_for_x_and_y_value(x, y):
    x = (x / transform_factor)  # offset because layout count starts with 1
    y = (y / transform_factor)  # yet another correction... zero point of y axis in game code is at the top left

    return coordinates.index((x, y, z))
