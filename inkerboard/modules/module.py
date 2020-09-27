from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from inkerboard.core.config import config
from inkerboard.utils.utils import Utils


class Module(object):
    # Predefined colors
    BLACK = 0
    GRAY = 127
    WHITE = 255

    FONT_DIR = Path.joinpath(Utils.project_root(), 'assets', 'fonts')

    def __init__(self, background=WHITE):
        self.width = int(config.display.width / 2)
        self.height = int(config.display.height / 2)
        self.module = self.__clear_module(background)
        self.draw = ImageDraw.Draw(self.module)

        self.font_icon_notice_size = int(self.height / 2)

        self.text_font = ImageFont.truetype(
            str(Path.joinpath(self.FONT_DIR, 'lato', 'Lato-Black.ttf')), 32)

    def __clear_module(self, background):
        return Image.new('L', (self.width, self.height), background)

    @staticmethod
    def _multi_line_text_size(text, font):
        # Determine text size using a scratch image to support multi line text
        draw = ImageDraw.Draw(Image.new("L", (1, 1)))
        w_cal_str, h_cal_str = draw.textsize(text, font)
        return w_cal_str, h_cal_str

    def _right(self) -> int:
        return self._from_right(0)

    def _left(self) -> int:
        return self._from_left(0)

    def _top(self) -> int:
        return self._from_top(0)

    def _from_top(self, offset: int) -> int:
        return int(offset)

    def _from_right(self, offset: int) -> int:
        return int(self.width - offset)

    def _from_left(self, offset: int) -> int:
        return int(offset)

    def _vertical_center(self) -> int:
        return int(self.height / 2)

    def _horizontal_center(self) -> int:
        return int(self.width / 2)

    def _draw_icon(self, position, text, size, color):
        self.draw.text(position, text, font=self.icon_font(size), fill=color)


    def icon_font(self, size: int) -> ImageFont:
        return ImageFont.truetype(str(Path.joinpath(self.FONT_DIR, 'fontawesome', 'fa-solid-900.ttf')), size)

    def render(self):
        return self.module
