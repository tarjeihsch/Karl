class Panel:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def draw(self, canvas):
        for element in self.elements:
            element.draw(canvas)