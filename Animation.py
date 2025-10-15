from PIL import Image, ImageTk

from Direction import Direction

# F, L, R, B

class Animation:
    def __init__(self, path, frame_width, frame_height, scale):
        image = Image.open(path)

        self.frame = 0
        self.frames = {d: [] for d in [Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP]}
        self.frame_time = 0.1
        self.frame_timer = 0

        # One width covers one directional animation sequence.
        # Populate each direction with the sequence from each width

        directions = [Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP]

        for row, y in enumerate(range(0, image.height, frame_height)):
            direction = directions[row]
            for x in range(0, image.width, frame_width):
                frame = image.crop((x, y, x + frame_width, y + frame_height))
                frame = frame.resize((frame_width * scale, frame_height * scale))
                self.frames[direction].append(ImageTk.PhotoImage(frame))

    def reset(self):
        self.frame = 0
        self.frame_timer = 0

    def update(self, delta_time):
        self.frame_timer += delta_time
        if self.frame_timer > self.frame_time:
            self.frame = (self.frame + 1) % len(self.frames)
            self.frame_timer = 0

    def get(self, direction):
        return self.frames[direction][self.frame]