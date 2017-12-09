#! /usr/bin/env python3

from PIL import Image, ImageDraw

import random
import math

def get_random_pixel():
    """Return a random RGB value as a 3-tuple"""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def set_to_noise(img):
    """Replace the contents of the image with random static"""
    img.putdata([random.randint(0, 255) for p in range(img.width * img.height)])

def get_rgb_noise(width, height):
    """Return an Image with randomly colored pixels"""
    bands = [Image.new('L', (width, height)) for band in ('r', 'g', 'b')]
    for band in bands:
        set_to_noise(band)
    img = Image.merge('RGB', bands)
    return img

def blur(img):
    """Replace each non-border pixel with the average of its neighbors and return as a new image"""
    width = img.width
    height = img.height
    img2 = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img2)
    for y in range(1, height-1):
        for x in range(1, width-1):
            neighbors = [img.getpixel((x_offs, y_offs)) for x_offs in (x-1, x, x+1) for y_offs in (y-1, y, y+1)]
            avg_color = [math.floor(sum(p[i] for p in neighbors)/len(neighbors)) for i in (0, 1, 2)]
            avg_color = tuple(avg_color)
            draw.point((x,y), avg_color)
    return img2

if __name__ == "__main__":
    width = 800
    height = 600
    img = get_rgb_noise(width, height)
    for i in range(10):
        img = blur(img)
    img.show()
