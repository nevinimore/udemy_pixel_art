import os
from typing import Tuple

from collections import defaultdict
from PIL import Image
import colorsys
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict

im_file = 'gray.png'

oim = np.asarray(Image.open(im_file))
image_pixels = oim.reshape(-1, 4)
# %%


unique_colours = set()
color_to_position = defaultdict(lambda: [])
for i, row in enumerate(oim):
    for j, cell in enumerate(row):
        if cell[3] == 255:
            uni = cell[0]
            unique_colours.add(uni)
            color_to_position[uni].append((i, j))
            if not (cell[0] == cell[1] and cell[0] == cell[2]):
                print(f'error in {i, j}, cell: {cell}')

color_nd_to_position = {}
for nk, ok in enumerate(sorted(color_to_position)):
    color_nd_to_position[nk] = color_to_position[ok]


def color_maker(hue: int) -> Tuple[
    Tuple[int, int, int, int],
    Tuple[int, int, int, int],
    Tuple[int, int, int, int],
    Tuple[int, int, int, int]
]:
    return (
        make_color0(hue),
        make_color1(hue),
        make_color2(hue),
        make_color3(hue),)


def make_color3(hue: int) -> Tuple[int, int, int, int]:
    return hsv2rgba((hue + 5) % 360, 80, 100)


def make_color2(hue: int) -> Tuple[int, int, int, int]:
    return hsv2rgba(hue, 100, 100)


def make_color1(hue: int) -> Tuple[int, int, int, int]:
    return hsv2rgba((hue - 5) % 360, 100, 80)


def make_color0(hue: int) -> Tuple[int, int, int, int]:
    return hsv2rgba((hue - 10) % 360, 100, 40)


def hsv2rgba(h, s, v) -> Tuple[int, int, int, int]:
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)) + (255,)



def make_img_from_colours(cor: Tuple) -> np.ndarray:
    new_im = np.full(oim.shape, (0, 0, 0, 0), dtype='uint8')
    for color_nd, posis in color_nd_to_position.items():
        for i, j in posis:
            new_im[i, j] = cor[color_nd]
    return new_im


imgs_dir = 'output/images/'
gif_dir = 'output/animation/'

os.makedirs(imgs_dir, exist_ok=True)
os.makedirs(gif_dir, exist_ok=True)
colors: Dict = {hue: color_maker(hue) for hue in range(360)}
for hue, cor in colors.items():
    new_img = make_img_from_colours(cor)
    img = Image.fromarray(new_img)
    img.save(imgs_dir + f'img{hue:03d}.png')

