from Collider import Collider
from Player import Player
from Controller import PlayerController
from Scene import Scene


class Game:
    def __init__(self):
        self.scene = Scene("Assets/world.json")

        self.entities = []
        self.controllers = []
        self.colliders = []

        player = Player()
        player_controller = PlayerController()
        player_controller.possess(player)

        self.entities.append(player)
        self.controllers.append(player_controller)

        pass

    def tick(self, delta_time):
        for obj in self.entities:
            obj.tick(delta_time)

    def draw(self, canvas, delta_time):
        self.scene.draw(canvas)

        for obj in self.entities:
            obj.draw(canvas)

        for obj in self.colliders:
            if obj.debug_draw:
                obj.draw(canvas)