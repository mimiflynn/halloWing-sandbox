import board
import displayio
import time
import pulseio
import neopixel
from adafruit_slideshow import PlayBackOrder, SlideShow

pixels = neopixel.NeoPixel(board.D4, 30, brightness=.1)

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (255, 100, 120)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (80, 200, 175)
WHITE = (255, 255, 255)

colors = [PINK, RED, ORANGE, YELLOW, GREEN,
          CYAN, PURPLE, BLUE, LIGHT_BLUE, WHITE]

color = 0
colorsLen = len(colors) - 1

slideshow = SlideShow(board.DISPLAY,
                      folder="/images", loop=True,
                      order=PlayBackOrder.ALPHABETICAL)

while True:
    for i in range(len(pixels)):
        pixels[i] = colors[color]
        time.sleep(.001)
    time.sleep(1)

    if color == colorsLen:
        color = 0
    else:
        color = color + 1

    slideshow.advance()
