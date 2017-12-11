#! /usr/bin/env python3

from PIL import Image, ImageDraw

import photomancy

import random

if __name__ == "__main__":
    width, height = (800, 600)
    img = Image.new('L', (width, height))
    photomancy.set_to_noise(img)
    for i in range(5):
        img = photomancy.for_each_cell(photomancy.bw_push_func, img, cell_radius=3)
        img.show()

    img.save("output.png")
