from PIL import Image, ImageTk

class Texture2D:
    def __init__(self, path, frame_width, frame_height):
        self.image = Image.open(path)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = 1.0
        self.frames = []

        sheet_width, sheet_height = self.image.size
        cols = sheet_width // self.frame_width
        rows = sheet_height // self.frame_height

        for y in range(rows):
            for x in range(cols):
                left = x * self.frame_width
                top = y * self.frame_height
                right = left + self.frame_width
                bottom = top + self.frame_height

                frame = self.image.crop((left, top, right, bottom))
                if self.scale != 1.0:
                    frame = frame.resize((int(self.frame_width / 2), int(self.frame_height / 2)), Image.NEAREST)

                self.frames.append(ImageTk.PhotoImage(frame))