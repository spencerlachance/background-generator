import ctypes
import math
import os
from pathlib import Path

from natsort import natsorted
from PIL import Image

# The dimensions ratio of the screen that the background image will fill
RATIO = 16/9


def calculate_grid_dimensions(num_pics):
    """
    Calculate the dimensions of the grid of images that best fits the screen.

    :param num_pics: The number of images to arrange
    :return: A tuple containing the width and height of the grid
    """
    width = 0
    prev_diff = 100
    diff = 99
    # Until the dimensions are as close to the RATIO defined above as possible, increase
    # the width and recalculate them
    while math.fabs(prev_diff) > math.fabs(diff):
        width += 1
        height = math.ceil(num_pics / width)
        prev_diff = diff
        diff = RATIO - width / height
    # Because the loop runs one extra time after finding the optimal dimensions
    width = width - 1
    return width, math.ceil(num_pics / width)    


def generate_bg(dir):
    """
    Read the images in the input directory, generate a desktop background from them, 
    and save it to a file.

    :param dir: Path to the directory containing the album arts for the background
    """
    pics = os.listdir(dir)
    pics = natsorted(pics)
    num_pics = len(pics)

    # Calculate the dimensions in number of pictures
    pics_width, pics_height = calculate_grid_dimensions(num_pics)

    print(f"The image will be {str(pics_width)} x {str(pics_height)} album arts.")

    # Calculate the dimensions of the final image in pixels
    # (Each album art will be forced to 250x250 pixels)
    pixel_width = pics_width * 250
    pixel_height = pics_height * 250

    print(
        f"The dimensions of the result image are {str(pixel_width)} x "
        f"{str(pixel_height)}"
    )

    # Build the resulting background image
    result = Image.new('RGB', (pixel_width, pixel_height))

    pics_idx = 0
    for y in range(pics_height):
        for x in range(pics_width):
            if pics_idx >= num_pics:
                break
            album_art = Image.open(Path(dir).joinpath(pics[pics_idx]))
            result.paste(album_art.resize((250, 250)), (x * 250, y * 250))
            pics_idx += 1

    result.save(Path("results").joinpath(f"{dir}.jpg"))


generate_bg("test")
