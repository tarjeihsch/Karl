from uib_inf100_graphics.event_app import run_app
import time
from Game import Game

def app_started(app):
    app.game = Game()
    app.pressed_keys = set()

    # Application time variables
    app.timer_delay = 16
    app.last_time = time.time()
    app.delta_time = 0.0
    pass

def key_pressed(app, event):
    app.pressed_keys.add(event.key)

def key_released(app, event):
    app.pressed_keys.discard(event.key)

def timer_fired(app):
    # Calculate time from last fixed step
    now = time.time()
    app.delta_time = now - app.last_time
    app.last_time = now

    if 'a' in app.pressed_keys:
        app.game.controllers[0].on_key_pressed("a")
    if 'd' in app.pressed_keys:
        app.game.controllers[0].on_key_pressed("d")
    if 'w' in app.pressed_keys:
        app.game.controllers[0].on_key_pressed("w")
    if 's' in app.pressed_keys:
        app.game.controllers[0].on_key_pressed("s")

    app.game.tick(app.delta_time)

    pass

def redraw_all(app, canvas):
    app.game.draw(canvas)

    pass

if __name__ == '__main__':
    run_app(width=1280, height=720)