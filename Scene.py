import json

from Player import Player


# A large issue with our framework TKinter is computational expensive draw call operations.
# Need to read all cubes from the json file to populate the static world map as data.
# Next is to convert all data into corresponding textures for their respective type (eg. Stone, Wall, Water).
# After this, we create a framebuffer and store the framebuffer as an image used to render the entire scene

import json
from PIL import Image, ImageTk

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
        # Load all tileset images from Tiled JSON
        for ts in self.data["tilesets"]:
            image_path = ts.get("image")
            if image_path:
                self.textures[ts["name"]] = Image.open(image_path)

    def load_triggers(self):
        # Tiled maps do not store triggers this way; leave placeholder
        pass

    def create_scene(self):
        layers = self.data["layers"]
        tile_size = self.data["tilewidth"]
        width = self.data["width"]
        height = self.data["height"]

        fb_width = width * tile_size
        fb_height = height * tile_size
        framebuffer = Image.new("RGBA", (fb_width, fb_height))

        # Build collision tile set
        collision_tiles = set()
        for ts in self.data["tilesets"]:
            firstgid = ts["firstgid"]
            for tile in ts.get("tiles", []):
                for prop in tile.get("properties", []):
                    if prop["name"] == "collision" and prop["value"]:
                        collision_tiles.add(tile["id"] + firstgid)

        # Render layers
        for layer in layers:
            if layer["type"] != "tilelayer":
                continue
            data = layer["data"]
            for y in range(height):
                for x in range(width):
                    gid = data[y * width + x]
                    if gid == 0:
                        continue

                    # Find tileset for gid
                    tileset = None
                    for ts in self.data["tilesets"]:
                        if gid >= ts["firstgid"]:
                            tileset = ts
                    if not tileset:
                        continue

                    image = self.textures.get(tileset["name"])
                    if not image:
                        continue

                    columns = tileset["columns"]
                    tile_w = tileset["tilewidth"]
                    tile_h = tileset["tileheight"]
                    local_id = gid - tileset["firstgid"]

                    sx = (local_id % columns) * tile_w
                    sy = (local_id // columns) * tile_h
                    tile_img = image.crop((sx, sy, sx + tile_w, sy + tile_h))
                    framebuffer.paste(tile_img, (x * tile_size, y * tile_size))

                    if gid in collision_tiles:
                        self.tiles.append(Tile(x * tile_size, y * tile_size))

        # Placeholder player entity logic
        player = Player()
        player.current_location = (0, 0)
        player.last_location = (0, 0)
        self.entities.append(player)

        self.framebuffer = framebuffer
        self.framebuffer_image = ImageTk.PhotoImage(self.framebuffer)
        print(f"Framebuffer: {(self.framebuffer.width * self.framebuffer.height * 4) / 1024 / 1024} MB")

    def draw(self, canvas):
        canvas.create_rectangle(0, 0, 1920, 1080, fill="#141413")
        canvas.create_image(0, 0, image=self.framebuffer_image, anchor="nw")

        #for tile in self.tiles:
        #    canvas.create_rectangle(tile.location[0], tile.location[1], tile.location[0] + 32, tile.location[1] + 32, outline="orange", width=4)