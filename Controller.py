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

    def on_key_pressed(self, event, sprinting):
        if event == "w":
            self.entity.move(Direction.UP, sprinting)
        if event == "s":
            self.entity.move(Direction.DOWN, sprinting)
        if event == "a":
            self.entity.move(Direction.LEFT, sprinting)
        if event == "d":
            self.entity.move(Direction.RIGHT, sprinting)