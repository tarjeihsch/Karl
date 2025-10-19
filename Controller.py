from Direction import Direction

class Controller:
    pass

class PlayerController(Controller):
    def __init__(self):
        self.entity = None

    def possess(self, entity):
        self.entity = entity

    def move_player(self, game, delta_time, event, sprinting):
        if event == "w":
            self.entity.move(game, delta_time, Direction.UP, sprinting)
        if event == "s":
            self.entity.move(game, delta_time, Direction.DOWN, sprinting)
        if event == "a":
            self.entity.move(game, delta_time, Direction.LEFT, sprinting)
        if event == "d":
            self.entity.move(game, delta_time, Direction.RIGHT, sprinting)

    def kill_player(self):
        self.entity.die()
