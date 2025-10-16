class Collider:
    def __init__(self, location, debug_draw):
        self.location = location
        self.debug_draw = debug_draw

    def draw(self, canvas):
        canvas.create_rectangle(self.location[0], self.location[1], self.location[0] + 64, self.location[1] + 64)