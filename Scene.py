import json
import random

from PIL import Image, ImageTk
from Enemy import Enemy
from Player import Player


class Tile:
    def __init__(self, x, y):
        self.location = (x, y)


class Trigger:
    def __init__(self, x, y, path):
        self.location = (x, y)
        self.path = path

class Consumable:
    def __init__(self, x, y, health):
        self.location = (x, y)
        self.health = health

class Scene:
    def __init__(self, filename: str):
        self.filename = filename
        self.triggers = []
        self.tiles = []
        self.consumables = []
        self.entities = []
        self.framebuffer = None
        self.framebuffer_image = None
        self.center_camera = True
        self.create_scene()
        self.last_camera_location = (0, 0)

    # Note: ChatGPT has been used to help design this JSON data parser
    def create_scene(self):
        with open(self.filename, "r") as f:
            data = json.load(f)

        tile_size = data["tilewidth"]
        width = data["width"]
        height = data["height"]
        fb_width = width * tile_size
        fb_height = height * tile_size

        textures = {}
        tilesets = data["tilesets"]

        for i in range(len(tilesets) - 1):
            for j in range(i + 1, len(tilesets)):
                if tilesets[i]["firstgid"] > tilesets[j]["firstgid"]:
                    tilesets[i], tilesets[j] = tilesets[j], tilesets[i]

        collision_tiles = set()
        collision_trigger = set()
        collision_consumables = set()

        for ts in tilesets:
            image_path = ts.get("image")
            if image_path:
                textures[ts["name"]] = Image.open(image_path).convert("RGBA")

            firstgid = ts["firstgid"]
            for tile in ts.get("tiles", []):
                props = {p["name"]: p["value"] for p in tile.get("properties", [])}
                if props.get("collision"):
                    collision_tiles.add(tile["id"] + firstgid)
                if props.get("path"):
                    collision_trigger.add(tile["id"] + firstgid)
                if props.get("consumable"):
                    collision_consumables.add(tile["id"] + firstgid)

        gid_to_tileset = []
        for i, ts in enumerate(tilesets):
            next_gid = tilesets[i + 1]["firstgid"] if i + 1 < len(tilesets) else 10**9
            gid_to_tileset.append((range(ts["firstgid"], next_gid), ts))

        framebuffer = Image.new("RGBA", (fb_width, fb_height), (0, 0, 0, 0))

        for layer in data["layers"]:
            if layer["type"] != "tilelayer":
                continue

            layer_data = layer["data"]
            layer_img = Image.new("RGBA", (fb_width, fb_height), (0, 0, 0, 0))
            paste = layer_img.paste

            for idx, gid in enumerate(layer_data):
                if gid == 0:
                    continue

                tileset = next((ts for rng, ts in gid_to_tileset if gid in rng), None)
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

                x = (idx % width) * tile_size
                y = (idx // width) * tile_size
                paste(tile_img, (x, y), tile_img)

                if gid in collision_tiles:
                    self.tiles.append(Tile(x, y))
                elif gid in collision_trigger:
                    self.triggers.append(Trigger(x, y, "cave.json"))
                elif gid in collision_consumables:
                    self.consumables.append(Consumable(x, y, 10))

            framebuffer = Image.alpha_composite(framebuffer, layer_img)

        props = {p["name"]: p["value"] for p in data.get("properties", [])}
        start_x = props.get("start_location_x", 0)
        start_y = props.get("start_location_y", 0)

        if props.get("monster"):
            for i in range(0, 1):
                en = Enemy()
                en.current_location = (random.randint(350, 500 + 250), random.randint(500, 500 + 250))
                self.entities.append(en)

        player = Player()
        player.current_location = (start_x, start_y)
        player.last_location = (start_x, start_y)
        self.entities.append(player)

        self.framebuffer = framebuffer
        self.framebuffer_image = ImageTk.PhotoImage(framebuffer)
        print(f"Framebuffer: {(fb_width * fb_height * 4) / 1024 / 1024:.2f} MB")

    def tick(self):
        player = None
        for entity in self.entities:
            if isinstance(entity, Player):
                player = entity

        if player is None:
            return

        self.last_camera_location = player.current_location

    def draw(self, canvas):
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        fb_w = self.framebuffer_image.width()
        fb_h = self.framebuffer_image.height()

        offset_x = w / 2 - self.last_camera_location[0]
        offset_y = h / 2 - self.last_camera_location[1]

        canvas.create_rectangle(0, 0, w, h, fill="black", outline="")
        canvas.create_image(offset_x, offset_y, image=self.framebuffer_image, anchor="nw")

        for entity in self.entities:
            entity.draw(canvas, offset_x, offset_y)
