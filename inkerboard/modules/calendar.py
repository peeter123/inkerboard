import calendar
from pathlib import Path
from datetime import datetime
from PIL import ImageFont
from inkerboard.core.config import config
from inkerboard.modules.module import Module


class Calendar(Module):
    def __init__(self):
        super().__init__(background=self.BLACK)

        self.firstweekday = config.modules.calendar.firstweekday
        self.showmonth = config.modules.calendar.showmonth

        self.font_cal_str_size = int(self.height / 9)
        self.font_cal_str = ImageFont.truetype(str(Path.joinpath(self.FONT_DIR, 'ubuntu-mono',
                                                                 'UbuntuMono-Bold.ttf')), self.font_cal_str_size)

    def render(self):
        time = datetime.now()

        # Generate calendar for current month
        cal_month_cal = calendar.TextCalendar(self.firstweekday).formatmonth(time.year, time.month)

        if self.showmonth:
            cal_month_cal = '{}\n\n{}'.format(cal_month_cal.split('\n', 1)[0].strip(), cal_month_cal.split('\n', 1)[-1])
        else:
            cal_month_cal = cal_month_cal.split('\n', 1)[-1]

        # Determine calendar size using a scratch image.
        w_cal_str, h_cal_str = self._multi_line_text_size(cal_month_cal, self.font_cal_str)
        x_mon_str = self._horizontal_center() - (w_cal_str / 2)
        y_mon_str = self._vertical_center() - (h_cal_str / 2)

        self.draw.text((x_mon_str, y_mon_str), cal_month_cal, font=self.font_cal_str, fill=self.WHITE)

        return self.module
