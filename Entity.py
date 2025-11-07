from Animation import Animation
from Direction import Direction

class Entity:
    def __init__(self):
        self.health = 100
        self.animation: dict[str, Animation] = {}

        self.animation_state = None
        self.previous_animation_state = None

        self.current_direction = Direction.DOWN
        self.last_direction = Direction.DOWN

        self.last_location = (0, 0)
        self.current_location = (0, 0)

        self.movement_speed = 150.0
        self.movement_speed_multiplier = 1.75

        self.debug_draw = False

        self.collision_box_size = (64, 64)

    def tick(self, game, delta_time):
        if self.animation_state is None:
            return

        self.animation[self.animation_state].update(delta_time, self.current_direction)

        if self.animation[self.animation_state].is_finished(self.current_direction):
            if self.animation_state == "Death":
                game.remove_entity(self)
                return
            self.animation_state = self.previous_animation_state
            self.animation[self.animation_state].reset()

        if self.last_location == self.current_location:
            if self.animation_state not in ("Hurt", "Death", "Attack"):
                if self.animation_state != "Idle":
                    self.animation_state = "Idle"

        self.last_location = self.current_location
        self.last_direction = self.current_direction

    def draw(self, canvas, offset_x, offset_y):
        if self.animation_state is None:
            return
        canvas.create_image(offset_x + self.current_location[0], offset_y + self.current_location[1] - 16, image=self.animation[self.animation_state].get(self.current_direction), anchor="c")

    def move(self, game, delta_time, direction: Direction, sprint: bool):
        pass

    def die(self):
        self.health = 0
        self.animation_state = "Death"
        self.animation[self.animation_state].reset()

    def on_attacked(self):
        if not self.animation[self.animation_state].cycle:
            # As the Hurt animation is a non cyclic animation, we wait for the animation to finish before allowing a new attack.
            return

        self.health -= 10

        if self.health <= 0:
            self.die()
            return

        # Cache the prev. animation index to restore after Hurt is played
        self.previous_animation_state = self.animation_state

        self.animation_state = "Hurt"

        self.animation[self.animation_state].reset()