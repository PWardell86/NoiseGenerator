from pyglet import *
from NoiseGenerator import Noise

explosionApp = window.Window(200, 200)
drawBatch = graphics.Batch()
height = explosionApp.height
width = explosionApp.width
counter = 1
counterAdd = 1

newNoise = Noise(15, 10, (width, 100, height), -1, (-0.7, -1, 0), drawBatch)

@explosionApp.event
def on_draw():
    explosionApp.clear()
    drawBatch.draw()

def update(t):
    global counter, counterAdd
    if counter > 100:
        counter = 100
        counterAdd = -1
    elif counter < 0:
        counter = 0
        counterAdd = 1
    else:
        counter += counterAdd
    pixels = newNoise.generatePixels(counter)

clock.schedule(update)
app.run()