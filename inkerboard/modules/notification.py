from pathlib import Path
from PIL import ImageFont
from inkerboard.modules.module import Module


class Notification(Module):
    def __init__(self, message, icon):
        super().__init__(background=self.WHITE)

        self.icon = icon
        self.message = message

        self.font_icon_size = int(self.height / 3)
        self.font_message_size = int(self.height / 10)

        self.font_icon = self.icon_font(self.font_icon_size)
        self.font_message_str = ImageFont.truetype(str(Path.joinpath(self.FONT_DIR, 'roboto', 'Roboto-Light.ttf')),
                                                   self.font_message_size)

    def render(self):
        # The Notification Icon
        w_icon, h_icon = self.font_icon.getsize(self.icon)
        x_icon = self._horizontal_center() - (w_icon / 2)
        y_icon = int(self.height / 3) - (h_icon / 2)

        # The notification message
        w_messsage, h_message = self.font_message_str.getsize(self.message)
        x_message = self._horizontal_center() - (w_messsage / 2)
        y_message = self.height - int(self.height / 3) - (h_message / 2)

        self._draw_icon((x_icon, y_icon), self.icon, self.font_icon_size, self.BLACK)
        self.draw.text((x_message, y_message), self.message, font=self.font_message_str, fill=self.BLACK)

        return self.module
