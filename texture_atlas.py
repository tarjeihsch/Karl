from PIL import Image, ImageTk

from ui.element import UIElement


class Texture(UIElement):
    def __init__(self, x, y, tk_image):
        super().__init__(x, y, 0, 0)
        self.tk_image = tk_image
        self._pil_image = ImageTk.getimage(tk_image).copy()
        self._tk_image_ref = None

    def draw(self, canvas):
        canvas.create_image(self.x, self.y, anchor="nw", image=self.tk_image)

    # Caution: This function is very expensive due to the cost of modifying the byte data of an image directly on the CPU.
    # As the INF100 framework does not support proper GPU blitting, expect choppyness when modifying the image.
    def crop_width(self, ratio: float):
        ratio = max(0.0, min(1.0, ratio))
        w, h = self._pil_image.size
        new_w = max(1, int(w * ratio))
        cropped = self._pil_image.crop((0, 0, new_w, h))
        self.tk_image = ImageTk.PhotoImage(cropped)

class TextureAtlas:
    def __init__(self, path):
        self.image = Image.open(path)

    def sample_texture(self, x_start, y_start, x_end, y_end, size = 1):
        cropped = self.image.crop((x_start, y_start, x_end, y_end))
        (w, h) = cropped.size
        final = cropped.resize((int(w * size), int(h * size)), Image.NEAREST)
        tk_image = ImageTk.PhotoImage(final)
        return tk_image