import os
import skimage as sk


class ImageReader:
    SUPPORTED_EXTENSIONS = ['.png']

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
