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

    def on_key_pressed(self, game, delta_time, event, sprinting):
        if event == "w":
            self.entity.move(game, delta_time, Direction.UP, sprinting)
        if event == "s":
            self.entity.move(game, delta_time, Direction.DOWN, sprinting)
        if event == "a":
            self.entity.move(game, delta_time, Direction.LEFT, sprinting)
        if event == "d":
            self.entity.move(game, delta_time, Direction.RIGHT, sprinting)
        if event == "k":
            self.entity.die()