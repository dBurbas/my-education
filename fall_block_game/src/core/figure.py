from config.config import SHAPES

# TODO: typehints
# TODO: docstrings
class Figure:
    def __init__(self, x, y, shape_index):
        self.cord_x = x
        self.cord_y = y
        self.shape_index = shape_index
        # ?: нужен индекс или строка для словаря
        # ?: нужен отдельный список или словарь для цветов или еще добавить в словарь форм цвет
        self.shape = SHAPES[shape_index]
        self.rotations = [self.shape]
        self.rotate_state = 0
        current = self.rotations[0]
        for _ in range(3):
            current = [list(row) for row in zip(*current[::-1])]
            self.rotations.append(current)  
        

    def rotate(self):
        """Return a new rotated shape"""
        rotated = self.rotations[self.rotation_state]
        self.rotation_state = (self.rotation_state + 1) % 4
        
        return rotated