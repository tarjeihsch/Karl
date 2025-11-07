from PIL import Image, ImageTk

class Texture:
    def __init__(self, width, height):
        pass

class TextureAtlas:
    def __init__(self, path, items):
        self.image = Image.open(path)

        width, height = self.image.size
        cols = width // self.frame_width
        rows = height // self.frame_height

        for y in range(rows):
            for x in range(cols):
                left = x * self.frame_width
                top = y * self.frame_height
                right = left + self.frame_width
                bottom = top + self.frame_height

                frame = self.image.crop((left, top, right, bottom))
                self.frames.append(ImageTk.PhotoImage(frame))