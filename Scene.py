import json

from PIL import Image, ImageTk

from Player import Player


# A large issue with our framework TKinter is computational expensive draw call operations.
# Need to read all cubes from the json file to populate the static world map as data.
# Next is to convert all data into corresponding textures for their respective type (eg. Stone, Wall, Water).
# After this, we create a framebuffer and store the framebuffer as an image used to render the entire scene

class Tile:
    def __init__(self, x, y):
        self.location = (x, y)

class Trigger:
    def __init__(self, x, y, path):
        self.location = (x, y)
        self.path = path

class Scene:
    def __init__(self, filename: str):
        self.data = json.load(open(filename))
        self.textures = {}
        self.triggers = []
        self.tiles = []
        self.entities = []
        self.framebuffer = None
        self.framebuffer_image = None
        self.load_textures()
        self.load_triggers()
        self.create_scene()

    def load_textures(self):
        for texture in self.data["world"]["textures"]:
            self.textures[texture["name"]] = Image.open(texture["path"])

    def load_triggers(self):
        for trigger_group in self.data["world"]["trigger"]:
            for triggers in trigger_group.values():
                for trigger in triggers:
                    self.triggers.append(Trigger(trigger["pos"][0] * 64, trigger["pos"][1] * 64, trigger["path"]))

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
            block_type = tile["texture"]
            texture = self.textures.get(block_type)
            framebuffer.paste(texture, (x * tile_size, y * tile_size))
            if tile["collision"]:
                self.tiles.append(Tile(x * tile_size, y * tile_size))

        player = Player()
        player.current_location = self.data["world"]["start_location"]
        player.last_location = self.data["world"]["start_location"]

        self.entities.append(player)

        self.framebuffer = framebuffer
        self.framebuffer_image = ImageTk.PhotoImage(self.framebuffer)
        print(f"Framebuffer: {(self.framebuffer.width * self.framebuffer.height * 4) / 1024 / 1024} MB")

    def draw(self, canvas):
        canvas.create_rectangle(0, 0, 1920, 1080, fill="#141413")
        canvas.create_image(0, 0, image=self.framebuffer_image, anchor="nw")

        for tile in self.tiles:
            canvas.create_rectangle(tile.location[0], tile.location[1], tile.location[0] + 64, tile.location[1] + 64, outline="orange", width=4)