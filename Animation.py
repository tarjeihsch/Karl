from PIL import Image, ImageTk

class Animation:
    def __init__(self, path, frame_width, frame_height, scale):
        image = Image.open(path)

        self.frame = 0
        self.frames = []
        self.frame_time = 0.1
        self.frame_timer = 0

        for y in range(0, image.height, frame_height):
            for x in range(0, image.width, frame_width):
                frame = image.crop((x, y, x + frame_width, y + frame_height))
                frame = frame.resize((frame_width * scale, frame_height * scale))
                self.frames.append(ImageTk.PhotoImage(frame))

    def reset(self):
        self.frame = 0
        self.frame_timer = 0

    def update(self, delta_time):
        self.frame_timer += delta_time
        if self.frame_timer > self.frame_time:
            self.frame = (self.frame + 1) % len(self.frames)
            self.frame_timer = 0

    def get(self):
        return self.frames[self.frame]