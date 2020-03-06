class Character:

    def __init__(self, character, grid_width):
        self.character = character
        self.grid_width = grid_width - 1
        self.x_offset = self.grid_width

    # private:
    def __get_coordinates(self, x_offset):
        chars = []
        for y, row in enumerate(self.character):
            for x, col in enumerate(row):
                if col == 'x':
                    chars.append((x + x_offset, y))
        return chars

    def get_coordinates(self):
        self.char_coordinates = self.__get_coordinates(self.x_offset)
        self.char_coordinates = self.__remove_out_of_range_coordinates(self.char_coordinates)
        return self.char_coordinates

    def rotate(self):
        self.x_offset = self.x_offset - 1 if len(self.char_coordinates) > 2 else self.grid_width

    def __remove_out_of_range_coordinates(self, whole_char):
        whole_char = [x for x in whole_char if 0 <= x[0] <= self.grid_width]  # remove pixels outside the grid
        return whole_char
