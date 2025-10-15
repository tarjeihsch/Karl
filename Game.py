from Player import Player
from Controller import PlayerController

class Game:
    def __init__(self):
        self.entities = []
        self.controllers = []

        player = Player()
        player_controller = PlayerController()
        player_controller.possess(player)

        self.entities.append(player)
        self.controllers.append(player_controller)

        pass

    def tick(self, delta_time):
        for obj in self.entities:
            obj.tick(delta_time)

    def draw(self, delta_time):
        for obj in self.entities:
            obj.draw(delta_time)