import os
import numpy as np
from skimage import io

SUPPORTED_EXTENSIONS = ['.png']
WHITE_GRAYSCALE = 1


def _normalize_points(points: np.ndarray):
    """
    Rotates and moves points on complex plane to put strings ends on y=0

    :param points: numpy array of points positions represented as complex numbers
    :return: numpy array with points where ends are on y=0
    """
    points -= points[0]  # make an offset to start from (0, 0)
    first = points[0]
    last = points[len(points) - 1]
    diff = last - first  # vector from first point to last that represents incline of string
    rotation = diff.conj() / abs(diff)  # complex number that rotates (abs = 1) points to neglect incline (conj
    # makes rotation in opposite to incline direction)
    return points * rotation


def read_points(path: str, max_y=1):
    """
    Opens an image with string and represents it with points

    :param max_y: maximal value of y coordinate
    :param path: path of the image
    :return: a tuple (x, y) with numpy arrays of x and y points' coordinates
    """
    if not path:
        raise ValueError("String path mustn't be empty")

    if max_y <= 0:
        raise ValueError("max_y must be positive")

    file, extension = os.path.splitext(path)
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("File extension is not supported")

    if not os.path.exists(path):
        raise ValueError("This path doesn't exist")

    string = io.imread(path, as_gray=True)

    is_white = string < WHITE_GRAYSCALE

    top_nonwhite = is_white.argmax(axis=0)
    bot_nonwhite = len(is_white) - np.flipud(is_white).argmax(axis=0)

    points_y = len(is_white) / 2 - 1 / 2 * (top_nonwhite + bot_nonwhite)  # minus is added because
    # coordinate system is flipped
    points_x = np.array([i for i in range(len(points_y))])
    complex_points = points_x + 1j * points_y  # represent points as complex numbers
    complex_points = _normalize_points(complex_points)

    max_y_before = np.max(np.abs(complex_points.imag))
    print(max_y_before)
    scale_y = max_y / max_y_before

    return complex_points.real, complex_points.imag * scale_y


def main():
    path = 'test_image.png'
    x, y = read_points(path)
    import matplotlib.pyplot as plt
    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    main()
