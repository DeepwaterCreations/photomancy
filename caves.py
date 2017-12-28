#! /usr/bin/env python3

from PIL import Image, ImageDraw, ImagePalette

import photomancy

import random
import itertools
import math
from copy import deepcopy

def generate_palette_cycle(width, height):
    """Create a list of pixel palette values that cycle through available 
    values sequentially
    """
    data = [0 for p in range(width * height)]
    iterator = itertools.cycle(range(math.floor(768/3)))
    data = [next(iterator) for p in data]

def generate_edgesquiggles(width, height):
    """Create a list of pixel palette values that form layered edges"""
    data = [[0 if random.randrange(20) > 0 else random.randint(1, 10) for x in range(width)] 
            for y in range(height)]

    def get_neighborhood(source_data, x, y, radius=1):
        neighborhood = [source_data[y_offs][x_offs] for y_offs in range(y-radius, y+radius) 
                for x_offs in range(x-radius, x+radius)]
        return neighborhood

    new_data = deepcopy(data)
    cell_radius = 1

    for i in range(10):
        for y in range(cell_radius, height-cell_radius):
            for x in range(cell_radius, width-cell_radius):
                neighborhood = get_neighborhood(data, x, y, cell_radius)
                self_value = data[y][x]
                if self_value > 0:
                    neighborhood.append(self_value+1)
                max_neighbor = max(neighborhood)
                new_data[y][x] = max_neighbor
        data = deepcopy(new_data)
        new_data = deepcopy(data)

    return sum(data, [])

if __name__ == "__main__":
    width, height = (800, 600)
    # bands = [Image.new('L', (width, height)) for band in ('r', 'g', 'b')]
    # for band in bands:
    #     img_data = generate_data(width, height)
    #     band.putdata(img_data)
    # img = Image.merge('RGB', bands)
    img = Image.new('P', (width, height))
    img.putpalette([random.randint(0, 255) for c in range(768)])
    img_data = generate_edgesquiggles(width, height)
    # print(img_data)
    img.putdata(img_data)
    # img = img.convert(mode='RGB')
    
    # photomancy.set_to_noise(img)
    # for i in range(5):
    #     img = photomancy.for_each_cell(photomancy.rgb_push_func, img, cell_radius=3)
    img.show()

    img.save("output.png")
