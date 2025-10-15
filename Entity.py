from Animation import Animation
from Direction import Direction

class Entity:
    def __init__(self):
        super().__init__()

        self.animation: dict[int, Animation] = {
            0: Animation("Assets/Unarmed_Idle_with_shadow.png", 64, 64, 1)
        }

        self.animation_index = 0

        self.current_direction = None
        self.last_direction = None

        self.location = (0, 0)
        self.movement_speed = 10.0

    def update_animation(self, delta_time):
        self.animation[self.animation_index].update(delta_time)

    def tick(self, delta_time):
        self.update_animation(delta_time)

    def draw(self, canvas):
        canvas.create_image(self.location[0], self.location[1], image=self.animation[self.animation_index].get(), anchor="nw")

    def move(self, direction: Direction):
        x, y = self.location
        if direction == Direction.UP: y -= 1 * self.movement_speed
        if direction == Direction.DOWN: y += 1 * self.movement_speed
        if direction == Direction.LEFT: x -= 1 * self.movement_speed
        if direction == Direction.RIGHT: x += 1 * self.movement_speed

        self.location = x, y
        self.last_direction = self.current_direction
        self.current_direction = direction