from Animation import Animation
from Direction import Direction

class Entity:
    def __init__(self):
        self.health = 6
        self.animation: dict[str, Animation] = {}

        self.animation_index = None

        self.current_direction = Direction.DOWN
        self.last_direction = Direction.DOWN

        self.last_location = (0, 0)
        self.current_location = (0, 0)

        self.movement_speed = 150.0
        self.movement_speed_multiplier = 1.75

        self.debug_draw = False

    def tick(self, game, delta_time):
        if self.animation_index is None:
            return

        self.animation[self.animation_index].update(delta_time)

        if self.animation_index == "Death":
            return

        if self.last_location == self.current_location:
            if self.animation_index != "Idle":
                self.animation_index = "Idle"

        self.last_location = self.current_location
        self.last_direction = self.current_direction

    def draw(self, canvas, offset_x, offset_y):
        if self.animation_index is None:
            return
        canvas.create_image(offset_x + self.current_location[0], offset_y + self.current_location[1] - 16, image=self.animation[self.animation_index].get(self.current_direction), anchor="c")

    def move(self, game, delta_time, direction: Direction, sprint: bool):
        pass

    def die(self):
        self.health = 0
        self.animation_index = "Death"
        self.animation[self.animation_index].reset()