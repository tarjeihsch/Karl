from Direction import Direction

class Controller:
    pass

class PlayerController(Controller):
    def __init__(self):
        self.entity = None
        pass

    def possess(self, entity):
        self.entity = entity
        pass

    def on_key_pressed(self, event):
        if event.key == "w":
            self.entity.move(Direction.UP)
        if event.key == "s":
            self.entity.move(Direction.DOWN)
        if event.key == "a":
            self.entity.move(Direction.LEFT)
        if event.key == "d":
            self.entity.move(Direction.RIGHT)