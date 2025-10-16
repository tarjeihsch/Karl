import json

from PIL import Image, ImageTk


# A large issue with our framework TKinter is computational expensive draw call operations.
# Need to read all cubes from the json file to populate the static world map as data.
# Next is to convert all data into corresponding textures for their respective type (eg. Stone, Wall, Water).
# After this, we create a framebuffer and store the framebuffer as an image used to render the entire scene

class Tile:
    def __init__(self, x, y):
        self.location = (x, y)

class Scene:
    def __init__(self, filename: str):
        self.data = json.load(open(filename))
        self.textures = {
            "grass": Image.open("Assets/grass.png"),
            "floor": Image.open("Assets/floor.png"),
            "water": Image.open("Assets/water.png")
        }
        self.tiles = []
        self.framebuffer = None

        self.create_scene()

    def create_scene(self):
        tiles = self.data["world"]["tiles"]
        tile_size = 64

        max_x = max(tile["pos"][0] for tile in tiles)
        max_y = max(tile["pos"][1] for tile in tiles)
        fb_width = (max_x + 1) * tile_size
        fb_height = (max_y + 1) * tile_size

        framebuffer = Image.new("RGBA", (fb_width, fb_height))

        for tile in tiles:
            x, y = tile["pos"]
            block_type = tile["type"]
            texture = self.textures.get(block_type)
            framebuffer.paste(texture, (x * tile_size, y * tile_size))
            if tile["collision"]:
                self.tiles.append(Tile(x * tile_size, y * tile_size))

        self.framebuffer = framebuffer
        print(f"Framebuffer: {(self.framebuffer.width * self.framebuffer.height * 4) / 1024 / 1024} MB")

    def draw(self, canvas):
        canvas.create_rectangle(0, 0, 1920, 1080, fill="#d1fffb")
        canvas.create_image(0, 0, image=ImageTk.PhotoImage(self.framebuffer), anchor="nw")

        for tile in self.tiles:
            canvas.create_rectangle(tile.location[0], tile.location[1], tile.location[0] + 64, tile.location[1] + 64, outline="orange", width=4)