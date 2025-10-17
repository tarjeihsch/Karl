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
        self.filename = filename
        self.triggers = []
        self.tiles = []
        self.entities = []
        self.framebuffer = None
        self.framebuffer_image = None
        self.create_scene()

    def create_scene(self):
        data = json.load(open(self.filename))
        textures = {}

        for ts in data["tilesets"]:
            image_path = ts.get("image")
            if image_path:
                textures[ts["name"]] = Image.open(image_path)

        layers = data["layers"]
        tile_size = data["tilewidth"]
        width = data["width"]
        height = data["height"]

        collision_tiles = set()
        collision_trigger = set()

        for ts in data["tilesets"]:
            firstgid = ts["firstgid"]
            for tile in ts.get("tiles", []):
                for prop in tile.get("properties", []):
                    if prop["name"] == "collision" and prop["value"]:
                        collision_tiles.add(tile["id"] + firstgid)
                    if prop["name"] == "path" and prop["value"]:
                        collision_trigger.add(tile["id"] + firstgid)

        fb_width = width * tile_size
        fb_height = height * tile_size
        framebuffer = Image.new("RGBA", (fb_width, fb_height), (0, 0, 0, 0))

        tilesets = sorted(data["tilesets"], key=lambda t: t["firstgid"])

        for layer in layers:
            if layer["type"] != "tilelayer":
                continue

            layer_img = Image.new("RGBA", (fb_width, fb_height), (0, 0, 0, 0))
            layer_data = layer["data"]

            for y in range(height):
                for x in range(width):
                    gid = layer_data[y * width + x]
                    if gid == 0:
                        continue

                    tileset = None
                    for i, ts in enumerate(tilesets):
                        next_gid = tilesets[i + 1]["firstgid"] if i + 1 < len(tilesets) else float("inf")
                        if ts["firstgid"] <= gid < next_gid:
                            tileset = ts
                            break
                    if not tileset:
                        continue

                    image = textures.get(tileset["name"])
                    if not image:
                        continue

                    columns = tileset["columns"]
                    tile_w = tileset["tilewidth"]
                    tile_h = tileset["tileheight"]
                    local_id = gid - tileset["firstgid"]

                    sx = (local_id % columns) * tile_w
                    sy = (local_id // columns) * tile_h
                    tile_img = image.crop((sx, sy, sx + tile_w, sy + tile_h))

                    # paste tile into this layer image using its own alpha
                    layer_img.paste(tile_img, (x * tile_size, y * tile_size), tile_img)

                    # blend this layer on top of the main framebuffer
                    framebuffer = Image.alpha_composite(framebuffer, layer_img)

                    if gid in collision_tiles:
                        self.tiles.append(Tile(x * tile_size, y * tile_size))

                    if gid in collision_trigger:
                        self.triggers.append(Trigger(x * tile_size, y * tile_size, "cave.json"))

        player = Player()
        player.current_location = (0, 0)
        player.last_location = (0, 0)
        self.entities.append(player)

        self.framebuffer = framebuffer
        self.framebuffer_image = ImageTk.PhotoImage(self.framebuffer)
        print(f"Framebuffer: {(self.framebuffer.width * self.framebuffer.height * 4) / 1024 / 1024} MB")

    def draw(self, canvas):
        canvas.create_rectangle(0, 0, 2560, 1600, fill="#141413")
        canvas.create_image(0, 0, image=self.framebuffer_image, anchor="nw")

        #for tile in self.tiles:
        #    canvas.create_rectangle(tile.location[0], tile.location[1], tile.location[0] + 32, tile.location[1] + 32, outline="orange", width=4)