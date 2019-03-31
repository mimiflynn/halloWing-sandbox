import board
import displayio
import time
import pulseio
import touchio
import os
import neopixel

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

pixels = neopixel.NeoPixel(board.D4, 30, brightness=.1)
pixels[0] = RED

forward_button = touchio.TouchIn(board.TOUCH4)
back_button = touchio.TouchIn(board.TOUCH1)

brightness_up = touchio.TouchIn(board.TOUCH3)
brightness_down = touchio.TouchIn(board.TOUCH2)

#backlight = pulseio.PWMOut(board.TFT_BACKLIGHT)
splash = displayio.Group()
board.DISPLAY.show(splash)

max_brightness = 2 ** 15

images = list(filter(lambda x: x.endswith("bmp"), os.listdir("/")))
i = 0


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 85:
        return (int(pos * 3), int(255 - (pos * 3)), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - (pos * 3)), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int((i * 256 / len(pixels)) + j * 10)
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(wait)


while True:

    rainbow_cycle(.001)

    forward = False
    backward = False

    with open(images[i], "rb") as f:
        try:
            odb = displayio.OnDiskBitmap(f)
        except ValueError:
            print("Image unsupported {}".format(images[i]))
            del images[i]
            continue
        face = displayio.TileGrid(
            odb, pixel_shader=displayio.ColorConverter(), x=0, y=0)
        splash.append(face)
        # Wait for the image to load.
        board.DISPLAY.wait_for_frame()

        # Fade up the backlight
        for b in range(100):
            #backlight.duty_cycle = b * max_brightness // 100
            time.sleep(0.01)

        # Wait forever
        while not forward and not backward:
            forward = forward_button.value
            backward = back_button.value

            if brightness_up.value:
                max_brightness += 16
            elif brightness_down.value:
                max_brightness -= 16
            if max_brightness < 0:
                max_brightness = 0
            elif max_brightness >= 2 ** 16:
                max_brightness = 2 ** 16 - 1
            #backlight.duty_cycle = max_brightness

        # Fade down the backlight
        for b in range(50, -1, -1):
            #backlight.duty_cycle = b * max_brightness // 100
            time.sleep(0.005)

        splash.pop()

        if forward:
            i += 1
        elif backward:
            i -= 1
        i %= len(images)
