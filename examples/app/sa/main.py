import os.path
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import PreText, Select
from bokeh.plotting import figure
from bokeh.models.widgets import Button
from bokeh.events import ButtonClick, Pan, PanEnd, Pinch
from bokeh.models.ranges import Range1d

apo_data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'log_test_1hours.txt'), header=0,
                       names=['date', 'time', 'coill', 'coilr', 'rooml', 'roomr', 'attl', 'attr', 'tatt'],
                       parse_dates=[['date', 'time']],
                       index_col='date_time')

min_time = apo_data.index.astype('int64').min() / 1000000
max_time = apo_data.index.astype('int64').max() / 1000000

data_len = len(apo_data)
time_len = max_time - min_time
# point_step = time_len / len(apo_data)

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
    start = ts1.x_range.start
    end = ts1.x_range.end
    print('start {} {}'.format(start, pd.to_datetime(start, unit='ms')))
    print('end   {} {}'.format(end,   pd.to_datetime(end,   unit='ms')))

    start_index = int(data_len * ((start - min_time) / time_len))
    start_index = max(0, start_index)

    end_index = int(data_len * ((end - min_time) / time_len))
    end_index = min(data_len, end_index)


    step = max(1, int((end_index - start_index) / 900))

    print('step', step)
    print('index {}'.format((start_index, end_index)))
    print(apo_data.iloc[int(start_index)])
    source.data = source.from_df(apo_data.iloc[start_index:end_index:step])


def pinch_event_hdlr(event):
    print('PINCH: {}'.format(vars(event)))

def range_callback(param, old, new):
    print('RANGE: Param: {}, old: {}, new: {}'.format(param, old, new))
    print(pd.to_datetime(new, unit='ms'))
    print(min_time, max_time)
    pos = new - min_time
    index = int(data_len * (pos / time_len))
    print('index', index)
    print(apo_data.iloc[int(index)])
    source.data = source.from_df(apo_data.iloc[int(index):])


source = ColumnDataSource(data=dict(date_time=[], coill=[]))
source.data = source.from_df(apo_data.iloc[::10000])

# x_range = Range1d(apo_data.date_time.min(), apo_data.date_time.max(), bounds='auto')
x_range = None
ts1 = figure(plot_width=900, plot_height=400, x_axis_type='datetime', x_range=x_range,
             tools = "pan,box_zoom,reset,wheel_zoom")
ts1.line('date_time', 'coill', source=source)

# ts1.x_range.on_change('start', range_callback)
# ts1.x_range.on_change('end', range_callback)

ts1.on_event(PanEnd, pan_event_hdlr)
# ts1.on_event(Pinch, pinch_event_hdlr)


button_plus  = Button(label='+', button_type="success")
button_minus = Button(label='-', button_type="success")

button_plus.on_event(ButtonClick, button_plus_click)
button_minus.on_event(ButtonClick, button_minus_click)

buttons_column = column([button_plus, button_minus])
# button.on_change('')

# ts1.x_range.on_change('end', printer_callback)
# ts1.x_range.on_change('start', printer_callback)

curdoc().add_root(row([ts1, buttons_column]))
