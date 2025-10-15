from uib_inf100_graphics.event_app import run_app
import time
from Game import Game

def app_started(app):
    app.game = Game()

    # Application time variables
    app.timer_delay = 16
    app.last_time = time.time()
    app.delta_time = 0.0
    pass

def key_pressed(app, event):
    app.game.controllers[0].on_key_pressed(event)
    pass

def timer_fired(app):
    # Calculate time from last fixed step
    now = time.time()
    app.delta_time = now - app.last_time
    app.last_time = now

    app.game.tick(app.delta_time)

    pass

def redraw_all(app, canvas):
    app.game.draw(canvas)

    pass

if __name__ == '__main__':
    run_app(width=1280, height=720)