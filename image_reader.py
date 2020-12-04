import os
import cmath
import skimage as sk
import numpy as np
from skimage import io


class ImageReader:
    SUPPORTED_EXTENSIONS = ['.png']
    WHITE_GRAYSCALE = 1

    def __init__(self, path: str):
        if not path:
            raise ValueError("String path mustn't be empty")

        file, extension = os.path.splitext(path)
        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError("File extension is not supported")

        self._path = path

    def read(self):
        assert self._path

        if not os.path.exists(self._path):
            raise ValueError("This path doesn't exist")

        string = io.imread(self._path, as_gray=True)
        print(string.shape)
        is_white = string < self.WHITE_GRAYSCALE
        top_nonwhite = is_white.argmax(axis=0)
        bot_nonwhite = len(is_white) - np.flipud(is_white).argmax(axis=0)
        print(bot_nonwhite - top_nonwhite)
        points_y = - 1/2 * (top_nonwhite + bot_nonwhite)  # minus is added because coordinate system is flipped
        points_x = np.array([i for i in range(len(points_y))])
        points = points_x + 1j * points_y  # represent points as complex numbers


if __name__ == "__main__":
    path = 'test_image.png'
    reader = ImageReader(path)
    reader.read()


