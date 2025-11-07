from Animation import Animation
from Direction import Direction
from Entity import Entity
from texture2d import Texture2D

class Player(Entity):
    def __init__(self):
        super().__init__()

        self.animation: dict[str, Animation] = {
            "Idle": Animation("assets/Player/PNG/Swordsman_lvl1/With_shadow/Swordsman_lvl1_Idle_with_shadow.png", 64, 64, 2, [(Direction.DOWN, 12), (Direction.LEFT, 12), (Direction.RIGHT, 12), (Direction.UP, 4)]),
            "Walk": Animation("assets/Player/PNG/Swordsman_lvl1/With_shadow/Swordsman_lvl1_Walk_with_shadow.png", 64, 64, 2, [(Direction.DOWN, 6), (Direction.LEFT, 6), (Direction.RIGHT, 6), (Direction.UP, 6)]),
            "Run": Animation("assets/Player/PNG/Swordsman_lvl1/With_shadow/Swordsman_lvl1_Run_with_shadow.png", 64, 64, 2, [(Direction.DOWN, 8), (Direction.LEFT, 8), (Direction.RIGHT, 8), (Direction.UP, 8)]),
            "Attack": Animation("assets/Player/PNG/Swordsman_lvl1/With_shadow/Swordsman_lvl1_attack_with_shadow.png", 64, 64, 2, [(Direction.DOWN, 8), (Direction.LEFT, 8), (Direction.RIGHT, 8), (Direction.UP, 8)], False),
            "Hurt": Animation("assets/Player/PNG/Swordsman_lvl1/With_shadow/Swordsman_lvl1_Hurt_with_shadow.png", 64, 64, 2, [(Direction.DOWN, 5), (Direction.LEFT, 5), (Direction.RIGHT, 5), (Direction.UP, 5)]),
            "Death": Animation("assets/Player/PNG/Swordsman_lvl1/With_shadow/Swordsman_lvl1_Death_with_shadow.png", 64, 64, 2, [(Direction.DOWN, 7), (Direction.LEFT, 7), (Direction.RIGHT, 7), (Direction.UP, 7)], False)
        }

        self.animation_state = "Idle"
        self.heart_texture = Texture2D("assets/Pixel Heart Sprite Sheet 32x32.png", 32, 32)

    def attack(self, game):
        if self.animation_state == "Attack":
            return

        self.animation_state = "Attack"
        self.previous_animation_state = "Idle"
        self.animation[self.animation_state].reset()

        x, y = self.current_location
        trace_end = self.current_location
        trace_length = 32 * 2

        # TODO: prefer using a switch
        if self.current_direction == Direction.UP:
            trace_end = (x, y - trace_length)
        elif self.current_direction == Direction.DOWN:
            trace_end = (x, y + trace_length)
        elif self.current_direction == Direction.LEFT:
            trace_end = (x - trace_length, y)
        elif self.current_direction == Direction.RIGHT:
            trace_end = (x + trace_length, y)

        for entity in game.scene.entities:
            if isinstance(entity, Player):
                # Skip self
                continue

            box_w, box_h = self.collision_box_size
            x1, y1 = self.current_location
            x2, y2 = trace_end

            min_x = min(x1, x2) - box_w / 2
            max_x = max(x1, x2) + box_w / 2
            min_y = min(y1, y2) - box_h / 2
            max_y = max(y1, y2) + box_h / 2

            if min_x <= entity.current_location[0] <= max_x and min_y <= entity.current_location[1] <= max_y:
                entity.on_attacked()

    def move(self, game, delta_time, direction: Direction, sprint: bool):
        if self.animation_state == "Attack":
            return

        super().move(game, delta_time, direction, sprint)
        x, y = self.current_location

        if sprint:
            self.animation_state = "Run"
            base_speed = self.movement_speed * self.movement_speed_multiplier
        else:
            self.animation_state = "Walk"
            base_speed = self.movement_speed

        if direction == Direction.UP: y -= 1 * base_speed * delta_time
        if direction == Direction.DOWN: y += 1 * base_speed * delta_time
        if direction == Direction.LEFT: x -= 1 * base_speed * delta_time
        if direction == Direction.RIGHT: x += 1 * base_speed * delta_time

        if self.current_direction != direction:
            # Reset animation counter, even when not playing the same sequence again
            # Start new animation depending on direction
            self.animation[self.animation_state].reset()

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