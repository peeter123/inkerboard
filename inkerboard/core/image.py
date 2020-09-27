from PIL import Image
from inkerboard.core.config import config


class EpaperImage(object):
    def __init__(self, modules: list):
        self.width = int(config.display.width)
        self.height = int(config.display.height)

        row1 = self._concat_h(modules[0], modules[1])
        row2 = self._concat_h(modules[2], modules[3])

        self.image = self._concat_v(row1, row2)

    @staticmethod
    def _concat_h(im1, im2):
        dst = Image.new('L', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst

    @staticmethod
    def _concat_v(im1, im2):
        dst = Image.new('L', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst

    def render(self):
        return self.image
