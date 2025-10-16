from Collider import Collider
from Player import Player
from Controller import PlayerController
from Scene import Scene


class Game:
    def __init__(self):
        self.scene = None
        self.controllers = []

        player_controller = PlayerController()
        self.controllers.append(player_controller)

        self.load_scene("world.json")

    def load_scene(self, path):
        self.scene = Scene(path)
        self.controllers[0].possess(self.scene.entities[0])

    def tick(self, delta_time):
        for obj in self.scene.entities:
            obj.tick(delta_time)

    def draw(self, canvas, delta_time):
        self.scene.draw(canvas)

        for obj in self.scene.entities:
            obj.draw(canvas)