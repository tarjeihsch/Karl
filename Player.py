from Animation import Animation
from Direction import Direction
from Entity import Entity
from texture2d import Texture2D

class Player(Entity):
    def __init__(self):
        super().__init__()

        self.animation: dict[str, Animation] = {
            "Idle": Animation("assets/Unarmed_Idle_with_shadow.png", 64, 64, 2),
            "Walk": Animation("assets/Unarmed_Walk_with_shadow.png", 64, 64, 2),
            "Run": Animation("assets/Unarmed_Run_with_shadow.png", 64, 64, 2),
            "Hurt": Animation("assets/Unarmed_Hurt_with_shadow.png", 64, 64, 2),
            "Death": Animation("assets/Unarmed_Death_with_shadow.png", 64, 64, 2, False)
        }

        self.animation_index = "Idle"
        self.heart_texture = Texture2D("assets/Pixel Heart Sprite Sheet 32x32.png", 32, 32)

    def move(self, game, delta_time, direction: Direction, sprint: bool):
        super().move(game, delta_time, direction, sprint)
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

    def draw(self, canvas, offset_x, offset_y):
        super().draw(canvas, offset_x, offset_y)

        w = canvas.winfo_width()
        h = canvas.winfo_height()
        self.health = 3
        self.max_health = 6
        hearts = self.max_health // 2  # 3 hearts

        for i in range(hearts):
            x = self.current_location[0] + 25 * (i + 1) + 96
            y = self.current_location[1] - 25
            heart_health = self.health - i * 2

            if heart_health >= 2:
                frame = self.heart_texture.frames[0]  # full
            elif heart_health == 1:
                frame = self.heart_texture.frames[1]  # half
            else:
                frame = self.heart_texture.frames[2]  # empty

            canvas.create_image(x, y, image=frame)