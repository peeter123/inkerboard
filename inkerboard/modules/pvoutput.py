import pvoutput
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageFont
from inkerboard.core.config import config
from inkerboard.modules.module import Module
from inkerboard.utils.utils import Utils
from inkerboard.utils.icons import Icons


class PVOutput(Module):
    def __init__(self):
        super().__init__(background=self.WHITE)

        # Module configuration
        self.pv_api_key = config.modules.pvoutput.api_key
        self.pv_system_id = config.modules.pvoutput.system_id
        self.pv_donate = config.modules.pvoutput.donate
        self.pv_timezone = config.modules.pvoutput.timezone

        self.pv_show_data = config.modules.pvoutput.show
        self.pv_extended_data = config.modules.pvoutput.extended

        # Initialize PVOutput connector
        self.pv = pvoutput.PVOutput(apikey=self.pv_api_key, systemid=self.pv_system_id, donation_made=self.pv_donate)

        # Set font sizes for use in this module
        self.font_pv_icon_size = int(self.height / 8)
        self.font_pv_title_size = int(self.height / 10)
        self.font_pv_data_size = int(self.height / 15)

        # Set fonts used in this module
        self.font_pv_title = ImageFont.truetype(str(Path.joinpath(self.FONT_DIR, 'roboto', 'Roboto-Light.ttf')),
                                                self.font_pv_title_size)
        self.font_pv_data = ImageFont.truetype(str(Path.joinpath(self.FONT_DIR, 'roboto', 'Roboto-Light.ttf')),
                                               self.font_pv_data_size)

        # Define slots for drawing text data
        self.slot_size_x = self.width / 2
        self.slot_size_y = self.height / 6
        self.slot_counter = 0

    def _draw_entry(self, icon, icon_size, text, text_size, color):
        pos_x = (self.slot_counter % 2) * self.slot_size_x
        pos_y = (self.slot_counter > 1) * self.slot_size_y + self.height / 6

        # Draw icon based on position
        w_icon, h_icon = self.icon_font(icon_size).getsize(icon)
        x_icon = pos_x + (self.slot_size_x / 3) - (w_icon / 2)
        y_icon = pos_y + (self.slot_size_y / 2) - (h_icon / 2)
        self.draw.text((x_icon, y_icon), icon, font=self.icon_font(icon_size), fill=color)

        # Draw text based on position
        w_text, h_text = self._multi_line_text_size(text, self.font_pv_data)
        x_text = pos_x + self.slot_size_x - (self.slot_size_x / 3) - (w_text / 2)
        y_text = pos_y + self.slot_size_y - (self.slot_size_y / 2) - (h_text / 2)
        self.draw.text((x_text, y_text), text, font=self.font_pv_data, fill=color)

        # Increase slot counter
        self.slot_counter += 1

    def render(self):
        time = datetime.today()
        status = self.pv.getstatus(history=True)
        with open('status.json', 'w') as statusfile:
            statusfile.write(Utils.serialize_json(status))

        with open('status.json', 'r') as statusfile:
            status = Utils.deserialize_json(statusfile.read())

        # Convert to Pandas dataframe
        day_output = pd.DataFrame(status)
        day_output['timestamp'].dt = day_output['timestamp'].dt.tz_localize(self.pv_timezone, ambiguous='infer')
        day_output['v1'] = day_output['v1'].div(1000)
        day_output['v3'] = day_output['v3'].div(1000)

        # Create graph
        plt.rc('ytick', labelsize=8)
        plt.ylim(ymin=0)
        fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(self.width / 100, self.height / 100 / 2), sharey=True)

        ax2 = ax1.twinx()
        ax4 = ax3.twinx()
        ax1.get_shared_y_axes().join(ax1, ax3)
        ax2.get_shared_y_axes().join(ax2, ax4)

        # Plot data from dataset
        day_output.plot(kind='line', x='timestamp', y='v4', color='0', ax=ax1, legend=None)
        day_output.plot(kind='area', x='timestamp', y='v3', color='0.75', ax=ax2, legend=None)
        day_output.plot(kind='line', x='timestamp', y='v2', color='0', ax=ax3, legend=None)
        day_output.plot(kind='area', x='timestamp', y='v1', color='0.75', ax=ax4, legend=None)

        # Move line graphs to top
        ax1.set_zorder(2)
        ax1.set_facecolor("none")
        ax3.set_zorder(2)
        ax3.set_facecolor("none")

        for ax in fig.axes:
            # Set minimum y
            ax.set_ylim((0, None))
            # Remove top spines from graphs
            ax.spines['top'].set_visible(False)

        # Remove left / right spines from graphs depending on the axis
        ax1.spines['right'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax3.spines['left'].set_visible(False)
        ax4.spines['left'].set_visible(False)

        # Set visibility of tick labels
        ax1.get_xaxis().set_visible(False)
        ax3.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(True)
        ax2.get_yaxis().set_visible(False)
        ax3.get_yaxis().set_visible(False)
        ax4.get_yaxis().set_visible(True)

        # Set tick labels formatter
        axis_locator = MaxNLocator(nbins='auto', steps=[1, 2, 2.5, 5, 10], min_n_ticks=4)
        # ax1.yaxis.set_major_locator(axis_locator)
        # ax2.yaxis.set_major_locator(axis_locator)
        # ax3.yaxis.set_major_locator(axis_locator)
        # ax4.yaxis.set_major_locator(axis_locator)

        # Remove tick marks from middle axis
        ax2.tick_params(axis=u'both', which=u'both', length=0)
        ax3.tick_params(axis=u'both', which=u'both', length=0)

        # Enable tick labels on the right axis
        ax4.tick_params(axis='y', labelright=True)

        fig.canvas.draw()
        plot = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())

        # Write data to image
        self.module.paste(plot, (0, plot.height))

        # Draw title and separator line
        pv_title_str = 'PVOutput'
        w_title_str, h_title_str = self.font_pv_title.getsize(pv_title_str)
        x_title_str = self._horizontal_center() - (w_title_str / 2)
        y_title_str = int(self.height / 10) - (h_title_str / 2)
        self.draw.text((x_title_str, y_title_str), pv_title_str, font=self.font_pv_title, fill=self.BLACK)
        self.draw.line((0, int(self.height / 10) + (h_title_str / 2) + 2, self.width,
                        int(self.height / 10) + (h_title_str / 2) + 2), fill=128)

        # Draw Icons with data
        if self.pv_show_data['generation']:
            pv_gen = f'{day_output.head(1)["v2"].item():.0f} W\n{day_output.head(1)["v1"].item():.2f} kWh'
            self._draw_entry(Icons.SUN, self.font_pv_icon_size, pv_gen, 25, self.BLACK)

        if self.pv_show_data['consumption']:
            pv_use = f'{day_output.head(1)["v4"].item():.0f} W\n{day_output.head(1)["v3"].item():.2f} kWh'
            self._draw_entry(Icons.PLUG, self.font_pv_icon_size, pv_use, 25, self.BLACK)

        if self.pv_show_data['gas']:
            gas_delta = day_output.head(1)[self.pv_extended_data['gas']].item() - \
                        day_output.tail(1)[self.pv_extended_data['gas']].item()
            pv_gas = f'{gas_delta:.2f} m3'
            self._draw_entry(Icons.BURN, self.font_pv_icon_size, pv_gas, 25, self.BLACK)

        if self.pv_show_data['water']:
            water_delta = day_output.head(1)[self.pv_extended_data['water']].item() - \
                        day_output.tail(1)[self.pv_extended_data['water']].item()
            pv_water = f'{water_delta:.2f} m3'
            self._draw_entry(Icons.WATER, self.font_pv_icon_size, pv_water, 25, self.BLACK)

        return self.module
