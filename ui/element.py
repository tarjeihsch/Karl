class UIElement:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True

    def draw(self, canvas):
        pass

    def update(self, delta_time):
        pass

    def handle_event(self, event):
        pass

    def is_hovered(self, mouse_pos):
        (mx, my) = mouse_pos
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height