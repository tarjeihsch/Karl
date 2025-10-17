from Animation import Animation
from Direction import Direction

class Entity:
    def __init__(self):
        super().__init__()

        self.animation: dict[str, Animation] = {
            "Idle": Animation("assets/Unarmed_Idle_with_shadow.png", 64, 64, 2),
            "Walk": Animation("assets/Unarmed_Walk_with_shadow.png", 64, 64, 2),
            "Run": Animation("assets/Unarmed_Run_with_shadow.png", 64, 64, 2),
            "Hurt": Animation("assets/Unarmed_Hurt_with_shadow.png", 64, 64, 2),
            "Death": Animation("assets/Unarmed_Death_with_shadow.png", 64, 64, 2, False)
        }

        self.health = 100

        self.animation_index = "Idle"

        self.current_direction = Direction.DOWN
        self.last_direction = Direction.DOWN

        self.last_location = (0, 0)
        self.current_location = (0, 0)

        self.movement_speed = 150.0
        self.movement_speed_multiplier = 1.75

        self.debug_draw = True

    def tick(self, delta_time):
        self.animation[self.animation_index].update(delta_time)

        if self.animation_index == "Death":
            return

        if self.last_location == self.current_location:
            if self.animation_index != "Idle":
                self.animation_index = "Idle"

        self.last_location = self.current_location
        self.last_direction = self.current_direction

    def draw(self, canvas):
        canvas.create_image(self.current_location[0], self.current_location[1] - 16, image=self.animation[self.animation_index].get(self.current_direction), anchor="c")

    def move(self, game, delta_time, direction: Direction, sprint: bool):
        x, y = self.current_location

        if sprint:
            self.animation_index = "Run"
            base_speed = self.movement_speed * self.movement_speed_multiplier
        else:
            self.animation_index = "Walk"
            base_speed = self.movement_speed

        if direction == Direction.UP: y -= 1 * base_speed * delta_time
        if direction == Direction.DOWN: y += 1 * base_speed * delta_time
        if direction == Direction.LEFT: x -= 1 * base_speed * delta_time
        if direction == Direction.RIGHT: x += 1 * base_speed * delta_time

        if self.current_direction != direction:
            # Reset animation counter, even when not playing the same sequence again
            # Start new animation depending on direction
            self.animation[self.animation_index].reset()

        for collider in game.scene.tiles:
            # If we are moving into a collider, abort
            if collider.location[0] <= x <= collider.location[0] + 32 and collider.location[1] <= y <= collider.location[1] + 32:
                return

        for trigger in game.scene.triggers:
            if trigger.location[0] <= x <= trigger.location[0] + 32 and trigger.location[1] <= y <= trigger.location[1] + 32:
                game.load_scene(trigger.path)

        self.current_location = x, y
        self.last_direction = self.current_direction
        self.current_direction = direction

    def die(self):
        self.health = 0
        self.animation_index = "Death"
        self.animation[self.animation_index].reset()