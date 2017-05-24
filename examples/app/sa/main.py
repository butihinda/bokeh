import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import PreText, Select
from bokeh.plotting import figure

apo_data = pd.read_csv('/Users/maximsivash/Downloads/bokeh/examples/app/sa/log_test_1hours.txt', header=0,
                       names=['date', 'time', 'coill', 'coilr', 'rooml', 'roomr', 'attl', 'attr', 'tatt'],
                       parse_dates=[['date', 'time']])

# print(apo_data.date_time)

import datetime

print(apo_data.iloc[::10000])

def printer_callback(param, old, new):
    global ts1
    global source
    # print('callback start')
    print('param {:<6}, old {}, new {}, diff {}'.format(param, old, new, new - old))
    print('start: {}, end: {}, diff: {}'.format(ts1.x_range.start, ts1.x_range.end, ts1.x_range.end - ts1.x_range.start))
    print('plot width {}'.format(ts1.plot_width))
    source.data = source.from_df(apo_data.iloc[150000:])
    # print('callback end')

source = ColumnDataSource(data=dict(date_time=[], coill=[]))
source.data = source.from_df(apo_data.iloc[::10000])

ts1 = figure(plot_width=900, plot_height=400, x_axis_type='datetime')
ts1.line('date_time', 'coill', source=source)

ts1.x_range.on_change('end', printer_callback)
ts1.x_range.on_change('start', printer_callback)

curdoc().add_root(column(ts1))