import os.path
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import PreText, Select
from bokeh.plotting import figure
from bokeh.models.widgets import Button
from bokeh.events import ButtonClick, Pan

apo_data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'log_test_1hours.txt'), header=0,
                       names=['date', 'time', 'coill', 'coilr', 'rooml', 'roomr', 'attl', 'attr', 'tatt'],
                       parse_dates=[['date', 'time']])


def printer_callback(param, old, new):
    global ts1
    global source
    # print('callback start')
    print('param {:<6}, old {}, new {}, diff {}'.format(param, old, new, new - old))
    print('start: {}, end: {}, diff: {}'.format(ts1.x_range.start, ts1.x_range.end, ts1.x_range.end - ts1.x_range.start))
    print('plot width {}'.format(ts1.plot_width))
    source.data = source.from_df(apo_data.iloc[150000:])
    # print('callback end')

offset = 0
step = 200000
len_ = 900

def right():
    global offset
    offset += step
    source.data = source.from_df(apo_data.iloc[offset : offset + len_ * int(step / len_): int(step / len_)])

def left():
    global offset
    offset -= step
    source.data = source.from_df(apo_data.iloc[offset : offset + len_ * int(step / len_) : int(step / len_)])

def button_plus_click(event):
    right()

def button_minus_click(event):
    left()

def pan_event_hdlr(event):
    print('PAN: {}'.format(vars(event)))

source = ColumnDataSource(data=dict(date_time=[], coill=[]))
source.data = source.from_df(apo_data.iloc[::10000])


ts1 = figure(plot_width=900, plot_height=400, x_axis_type='datetime')
ts1.line('date_time', 'coill', source=source)

ts1.on_event(Pan, pan_event_hdlr)

button_plus  = Button(label='+', button_type="success")
button_minus = Button(label='-', button_type="success")

button_plus.on_event(ButtonClick, button_plus_click)
button_minus.on_event(ButtonClick, button_minus_click)

buttons_column = column([button_plus, button_minus])
# button.on_change('')

# ts1.x_range.on_change('end', printer_callback)
# ts1.x_range.on_change('start', printer_callback)

curdoc().add_root(row([ts1, buttons_column]))
