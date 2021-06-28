"""
File: blur.py
Name: Victor
-------------------------------
This file shows the original image first,
smiley-face.png, and then compare to its
blurred image. The blur algorithm uses the
average RGB values of a pixel's nearest neighbors
"""

from simpleimage import SimpleImage

BLUR_TIMES = 4


def blur(img):
    """
    :param img: SimpleImage, the original picture
    :return new_img: SimpleImage, the picture with blur
    """
    new_img = SimpleImage.blank(img.width, img.height)
    for x in range(img.width):
        for y in range(img.height):
            red = 0
            green = 0
            blue = 0
            count = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    pixel_x = x + i
                    pixel_y = y + j
                    if 0 <= pixel_x < img.width:
                        if 0 <= pixel_y < img.height:
                            pixel = img.get_pixel(pixel_x, pixel_y)
                            red += pixel.red
                            green += pixel.green
                            blue += pixel.blue
                            count += 1
            new_pixel = new_img.get_pixel(x, y)
            new_pixel.red = red / count
            new_pixel.green = green / count
            new_pixel.blue = blue / count
    return new_img


def main():
    """
    Given a picture, and make the picture blur 5 times.
    """
    old_img = SimpleImage("images/smiley-face.png")
    old_img.show()

    blurred_img = blur(old_img)
    for i in range(BLUR_TIMES):
        blurred_img = blur(blurred_img)
    blurred_img.show()


if __name__ == '__main__':
    main()
