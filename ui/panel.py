class Panel:
    def __init__(self):
        self.elements = {}

    def add_element(self, name, element):
        self.elements[name] = element

    def get_element(self, name):
        return self.elements[name]

    def draw(self, canvas):
        for element in self.elements.values():
            element.draw(canvas)