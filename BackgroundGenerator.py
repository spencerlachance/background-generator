import os, math, ctypes
from PIL import Image
from natsort import natsorted

def generate_bg(dir):
    pics = os.listdir(dir)
    pics = natsorted(pics)
    num_pics = len(pics)

    # calculates the dimensions of the grid that will best fit the 16x9 ratio screen
    ratio = 16 / 9
    w = 1
    prev_diff = 100
    diff = 99
    while math.fabs(prev_diff) > math.fabs(diff):
        prev_diff = diff
        h = math.ceil(num_pics / w)
        diff = ratio - w / h
        w += 1

    # dimensions in number of pictures
    pics_width = w - 2
    pics_height = math.ceil(num_pics / pics_width)

    print("The image will be " + str(pics_width) + " x " + str(pics_height) + " arts")

    # dimensions of the final image in pixels
    result_width = pics_width * 250
    result_height = int(result_width * 9 / 16)

    if pics_height * 250 > result_height:
        result_height = pics_height * 250
        result_width = pics_width * 250

    print("The dimensions of the result image are " + str(result_width)
        + " x " + str(result_height))

    # builds the resulting background image
    result_height += math.ceil(result_height / 27)
    result = Image.new('RGB', (result_width, result_height))

    index = 0
    for y in range(pics_height):
        if index >= num_pics:
                break
        for x in range(pics_width):
            if index >= num_pics:
                break
            im = Image.open(dir + "\\" + pics[index])
            if x * 250 > result_width or y * 250 > result_height:
                print("ERROR")
            result.paste(im.resize((250, 250)), (x * 250, y * 250))
            index += 1

    result.save('results/' + dir + '.jpg')

# sets the image as the desktop background
# SPI_SETDESKWALLPAPER = 20 
# ctypes.windll.user32.SystemParametersInfoW(
#     SPI_SETDESKWALLPAPER, 0,
#     "C:\\Users\\Spencer LaChance\\Pictures\\Desktop Background\\result.jpg" , 0)

generate_bg("Arts1")
generate_bg("Arts2")
