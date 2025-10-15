from Animation import Animation
from Direction import Direction

class Entity:
    def __init__(self):
        super().__init__()

        self.animation: dict[str, Animation] = {
            "Idle": Animation("Assets/Unarmed_Idle_with_shadow.png", 64, 64, 2),
            "Walk": Animation("Assets/Unarmed_Walk_with_shadow.png", 64, 64, 2)
        }

        self.animation_index = "Idle"

        self.current_direction = Direction.DOWN
        self.last_direction = Direction.DOWN

        self.last_location = (0, 0)
        self.current_location = (0, 0)

        self.movement_speed = 2.0

    def tick(self, delta_time):
        self.animation[self.animation_index].update(delta_time)

        if self.last_location == self.current_location:
            if self.animation_index != "Idle":
                self.animation_index = "Idle"
        else:
            if self.animation_index != "Walk":
                self.animation_index = "Walk"

        self.last_location = self.current_location
        self.last_direction = self.current_direction

    def draw(self, canvas):
        canvas.create_image(self.current_location[0], self.current_location[1], image=self.animation[self.animation_index].get(self.current_direction), anchor="nw")

    def move(self, direction: Direction):
        x, y = self.current_location

        if direction == Direction.UP: y -= 1 * self.movement_speed
        if direction == Direction.DOWN: y += 1 * self.movement_speed
        if direction == Direction.LEFT: x -= 1 * self.movement_speed
        if direction == Direction.RIGHT: x += 1 * self.movement_speed

        if self.current_direction != direction:
            # Reset animation counter, even when not playing the same sequence again
            # Start new animation depending on direction
            self.animation[self.animation_index].reset()

        self.current_location = x, y
        self.last_direction = self.current_direction
        self.current_direction = direction