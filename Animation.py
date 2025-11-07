from PIL import Image, ImageTk

from Direction import Direction

# F, L, R, B

class Animation:
    def __init__(self, path, frame_width, frame_height, scale, frames, cycle = True):
        image = Image.open(path)

        self.frame = 0
        self.frames = {direction: [] for direction, _ in frames}
        self.frame_duration = 0.1
        self.frame_timer = 0
        self.cycle = cycle

        # One width covers one directional animation sequence.
        # Populate each direction with the sequence from each width

        for row, y in enumerate(range(0, image.height, frame_height)):
            if row >= len(frames):
                break

            direction, frame_count = frames[row]

            for i in range(frame_count):
                x = i * frame_width
                frame = image.crop((x, y, x + frame_width, y + frame_height))
                frame = frame.resize((frame_width * scale, frame_height * scale))
                self.frames[direction].append(ImageTk.PhotoImage(frame))

    def reset(self):
        self.frame = 0
        self.frame_timer = 0

    def update(self, delta_time, direction):
        frame_length = len(self.frames[direction])

        if not self.cycle and self.frame == frame_length - 1:
            return

        self.frame_timer += delta_time

        if self.frame_timer > self.frame_duration:
            self.frame = (self.frame + 1) % frame_length
            self.frame_timer = 0

    def get(self, direction):
        frames = self.frames[direction]
        if not frames:
            return None
        return frames[min(self.frame, len(frames) - 1)]

    def is_finished(self, direction):
        return not self.cycle and self.frame >= len(self.frames[direction]) - 1