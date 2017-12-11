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

def for_each_cell(func, img, cell_radius=1):
    """Call a function on groups of pixels in the source image and return a transformed image"""
    width = img.width
    height = img.height
    img2 = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img2)
    for y in range(cell_radius, height-cell_radius):
        for x in range(cell_radius, width-cell_radius):
            neighbors = [img.getpixel((x_offs, y_offs)) for x_offs in range(x-cell_radius, x+cell_radius+1) for y_offs in range(y-cell_radius, y+cell_radius+1)]
            func(img, draw, x, y, neighbors)
    return img2

def blur(img):
    """Replace each non-border pixel with the average of its neighbors and return as a new image"""
    def blur_func(img, draw, x, y, neighbors):
        avg_color = get_avg_color(neighbors)
        draw.point((x,y), avg_color)

    return for_each_cell(blur_func, img)

def get_avg_color(neighbors):
    return tuple([math.floor(sum(p[i] for p in neighbors)/len(neighbors)) for i in (0, 1, 2)])

def rgb_push_func(img, draw, x, y, neighbors):
    orig_color = img.getpixel((x, y))
    avg_color = get_avg_color(neighbors)
    max_band_val = max(avg_color)
    pushed_color = tuple(32 if v == max_band_val else -32 for v in avg_color)
    combined_color = tuple(min(255, v[0] + v[1]) for v in zip(orig_color, pushed_color))
    # combined_color = orig_color + pushed_color
    draw.point((x,y), combined_color)

def filter_color(color):
    if all([not(0 < v < 255) for v in color]):
        return tuple(0 if v == 255 else 255 for v in color)
    else:
        return color

if __name__ == "__main__":
    width = 800
    height = 600
    img = get_rgb_noise(width, height)
    for i in range(5):
        img = for_each_cell(rgb_push_func, img)
        img = for_each_cell(lambda img, draw, x, y, neighbors: draw.point((x, y), filter_color(img.getpixel((x, y)))), img, cell_radius=0)
        # img = blur(img)
    img.show()

    img.save("output.png")
