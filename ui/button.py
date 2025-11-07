from ui.element import UIElement

class Button(UIElement):
    def __init__(self, x, y, width, height, text, callback):
        super().__init__(x, y, width, height)

        self.text = text
        self.callback = callback
        self.hovered = False

    def draw(self, canvas):
        if not self.visible:
            return