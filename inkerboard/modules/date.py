from pathlib import Path
from datetime import datetime
from PIL import ImageFont
from inkerboard.modules.module import Module


class Date(Module):
    def __init__(self):
        super().__init__(background=self.BLACK)

        self.font_day_str_size = int(self.height / 6)
        self.font_day_nr_size = int(self.height / 2)
        self.font_mon_str_size = int(self.height / 10)

        self.font_day_str = ImageFont.truetype(str(Path.joinpath(self.FONT_DIR, 'roboto', 'Roboto-Light.ttf')),
                                               self.font_day_str_size)
        self.font_day_nr = ImageFont.truetype(str(Path.joinpath(self.FONT_DIR, 'roboto', 'Roboto-Black.ttf')),
                                              self.font_day_nr_size)
        self.font_mon_str = ImageFont.truetype(str(Path.joinpath(self.FONT_DIR, 'roboto', 'Roboto-Light.ttf')),
                                               self.font_mon_str_size)

    def render(self):
        time = datetime.now()

        # Date Strings
        cal_day_str = time.strftime("%A")
        cal_day_nr = time.strftime("%d")
        cal_mon_str = time.strftime("%B") + ' ' + time.strftime("%Y")

        # the Day string "Monday" for Example
        w_day_str, h_day_str = self.font_day_str.getsize(cal_day_str)
        x_day_str = self._horizontal_center() - (w_day_str / 2)
        y_day_str = int(self.height / 4) - (h_day_str / 2)

        # the settings for the Calenday today number
        w_day_num, h_day_num = self.font_day_nr.getsize(cal_day_nr)
        x_day_num = self._horizontal_center() - (w_day_num / 2)
        y_day_num = int(self.height / 2) - (h_day_num / 2)

        # the settings for the Calenday Month String
        w_mon_str, h_mon_str = self.font_mon_str.getsize(cal_mon_str)
        x_mon_str = self._horizontal_center() - (w_mon_str / 2)
        y_mon_str = self.height - int(self.height / 6) - (h_mon_str / 2)

        self.draw.text((x_day_str, y_day_str), cal_day_str, font=self.font_day_str, fill=self.WHITE)
        self.draw.text((x_day_num, y_day_num), cal_day_nr, font=self.font_day_nr, fill=self.WHITE)
        self.draw.text((x_mon_str, y_mon_str), cal_mon_str, font=self.font_mon_str, fill=self.WHITE)

        return self.module
