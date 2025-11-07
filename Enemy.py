import heapq
import random

from Animation import Animation
from Direction import Direction
from Entity import Entity
from Player import Player

def tile_from_pos(tile_size, pos):
    return int(pos[0] // tile_size), int(pos[1] // tile_size)

def pos_from_tile(tile_size, tile):
    return tile[0] * tile_size + tile_size / 2, tile[1] * tile_size + tile_size / 2

class Enemy(Entity):
    def __init__(self):
        super().__init__()

        # Randomly select one of three textures

        random_value = random.randint(1, 3)

        self.animation: dict[str, Animation] = {
            "Idle": Animation(f"assets/Enemy/PNG/Orc{random_value}/With_shadow/orc{random_value}_idle_with_shadow.png", 64, 64, 2, [(Direction.DOWN, 4), (Direction.UP, 4), (Direction.LEFT, 4), (Direction.RIGHT, 4)], True),
            "Walk": Animation(f"assets/Enemy/PNG/Orc{random_value}/With_shadow/orc{random_value}_walk_with_shadow.png", 64, 64, 2, [(Direction.DOWN, 6), (Direction.UP, 6), (Direction.LEFT, 6), (Direction.RIGHT, 6)], True),
            "Hurt": Animation(f"assets/Enemy/PNG/Orc{random_value}/With_shadow/orc{random_value}_hurt_with_shadow.png", 64, 64, 2, [(Direction.DOWN, 6), (Direction.UP, 6), (Direction.LEFT, 6), (Direction.RIGHT, 6)], False),
            "Death": Animation(f"assets/Enemy/PNG/Orc{random_value}/With_shadow/orc{random_value}_death_with_shadow.png", 64, 64, 2, [(Direction.DOWN, 8), (Direction.UP, 8), (Direction.LEFT, 8), (Direction.RIGHT, 8)], False),
            "Attack": Animation(f"assets/Enemy/PNG/Orc{random_value}/With_shadow/orc{random_value}_attack_with_shadow.png", 64, 64, 2, [(Direction.DOWN, 8), (Direction.UP, 8), (Direction.LEFT, 8), (Direction.RIGHT, 8)], False),
        }

        self.animation_state = "Idle"
        self.points = []
        self.has_target = False

    # Note: ChatGPT has been used to help design some parts of the A* pathfinding algorithm found in this function
    def move(self, game, delta_time, direction, sprint):
        if self.animation_state == "Hurt" or self.animation_state == "Death":
            return

        player = None
        for e in game.scene.entities:
            if isinstance(e, Player):
                player = e
                break
        if player is None:
            return

        min_distance = 64  # pixels
        max_distance = min_distance * 4

        dx = player.current_location[0] - self.current_location[0]
        dy = player.current_location[1] - self.current_location[1]
        distance_sq = dx * dx + dy * dy

        if distance_sq < min_distance * min_distance:
            # Already close enough; stop moving
            self.points = []

            player = None
            for entity in game.scene.entities:
                if isinstance(entity, Player):
                    player = entity
                    break

            if player is None:
                return

            if abs(dx) > abs(dy):
                if dx > 0:
                    self.current_direction = Direction.RIGHT
                else:
                    self.current_direction = Direction.LEFT
            else:
                if dy > 0:
                    self.current_direction = Direction.DOWN
                else:
                    self.current_direction = Direction.UP

            if self.animation_state != "Attack" and self.hurt_wait_timer > 1.5 and self.attack_wait_timer > 1:
                player.on_attacked()
                self.previous_animation_state = "Idle"
                self.animation_state = "Attack"
                self.animation[self.animation_state].reset()

            return

        if distance_sq > min_distance * min_distance and self.has_target:
            self.attack_wait_timer = 0

        if distance_sq > max_distance * max_distance and not self.has_target:
            self.points = []
            return

        tile_size = 32
        blocked = {(t.location[0] // tile_size, t.location[1] // tile_size) for t in game.scene.tiles}

        start = tile_from_pos(tile_size, self.current_location)
        goal = tile_from_pos(tile_size, player.current_location)

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal:
                break

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nxt = (current[0] + dx, current[1] + dy)
                if nxt in blocked or nxt in cost_so_far:
                    continue  # already visited or blocked

                new_cost = cost_so_far[current] + 1
                cost_so_far[nxt] = new_cost
                priority = new_cost + heuristic(goal, nxt)
                heapq.heappush(frontier, (priority, nxt))
                came_from[nxt] = current

        if goal not in came_from:
            self.points = []
            return

        path = []
        node = goal
        while node != start:
            path.append(node)
            node = came_from[node]
        path.reverse()
        self.points = path

        if not path:
            return

        self.has_target = True

        next_tile = path[0]
        tx, ty = pos_from_tile(tile_size, next_tile)
        x, y = self.current_location

        dx = tx - x
        dy = ty - y
        step = self.movement_speed * delta_time

        if abs(dx) > abs(dy):
            if abs(dx) > step:
                x += step if dx > 0 else -step
            else:
                x = tx

            if dx > 0:
                self.current_direction = Direction.RIGHT
            else:
                self.current_direction = Direction.LEFT
        else:
            if abs(dy) > step:
                y += step if dy > 0 else -step
            else:
                y = ty
            if dy > 0:
                self.current_direction = Direction.DOWN
            else:
                self.current_direction = Direction.UP

        self.current_location = (x, y)
        self.animation_state = "Walk"

    def tick(self, game, delta_time):
        super().tick(game, delta_time)

        self.move(game, delta_time, Direction.DOWN, False)

    def draw(self, canvas, offset_x, offset_y):
        super().draw(canvas, offset_x, offset_y)

        w = canvas.winfo_width()
        h = canvas.winfo_height()

        (x, y) = self.current_location

        (x, y) = self.current_location

        if self.has_target:
            bar_width = 75
            bar_height = 5
            health_ratio = max(0, min(1, self.health / 100))

            x0 = x + offset_x - 40
            y0 = y + offset_y - 60
            x1 = x0 + bar_width
            y1 = y0 - bar_height

            # Background
            canvas.create_rectangle(x0, y1, x1, y0, fill="gray", outline="black", width=1)
            # Foreground

            if self.health > 0:
                canvas.create_rectangle(x0, y1, x0 + bar_width * health_ratio, y0, fill="red", outline="")

        if self.debug_draw:
            tile_size = 32

            for tile in self.points:
                tx, ty = tile[0] * tile_size + tile_size / 2, tile[1] * tile_size + tile_size / 2
                x0, y0 = offset_x + tx - tile_size / 2, offset_y + ty - tile_size / 2
                x1, y1 = offset_x + tx + tile_size / 2, offset_y + ty + tile_size / 2
                canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=1)

    def on_attacked(self):
        super().on_attacked()

        (x, y) = self.current_location

        match self.current_direction:
            case Direction.UP:
                self.current_location = (x, y - 10)
            case Direction.DOWN:
                self.current_location = (x, y + 10)
            case Direction.LEFT:
                self.current_location = (x + 10, y)
            case Direction.RIGHT:
                self.current_location = (x - 10, y)

        self.hurt_wait_timer = 0

