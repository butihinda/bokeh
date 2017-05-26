import random
from collections import OrderedDict

from datetime import timedelta
from datetime import datetime as dtime

import pandas as pd
import numpy as np

np.set_printoptions(precision=5, suppress=True)
np.random.seed(1, )


def get_random_points(len):
    from numpy import interp
    from scipy.signal import medfilt
    data = np.zeros(len)

    points_n = int(len * 10 / (360000))

    data[np.random.choice(len, size=points_n)] = np.random.sample(points_n) * 20

    # for i in data: print(i)

    def nan_helper(y):
        return y == 0, lambda z: z.nonzero()[0]

    nans, x = nan_helper(data)

    data[nans] = np.interp(x(nans), x(~nans), data[~nans])

    data += 30

    # making some noise

    # zeros = np.zeros_like(data)
    # noise = np.random.normal(scale=1, size=data.size)

    # data =+ noise

    return data

hours_n = 24
N = hours_n * 360000

# np.random.rand(2, 3)

d = pd.date_range(dtime(2017, 3, 1, 0, 0, 0, 0),  periods=N, freq=timedelta(milliseconds=10))

dates = [i.date() for i in d]
times = [i.strftime('%H:%M:%S.%f') for i in d]

# temp_room = np.random.sample(N).cumsum() -0.5 * 3 + 30
temp_room = get_random_points(N)
temp_coil = temp_room + 1
exc = np.ones_like(temp_room)


df = pd.DataFrame(OrderedDict([
                ('DATE', dates),
                ('TIME', times),
                ('VOICE COIL L', temp_coil),
                ('VOICE COIL R', exc),
                ('ROOMT L', temp_room),
                ('ROOMT R', exc),
                ('EXCURSION ATT L', exc),
                ('EXCURSION ATT R', exc),
                ('THERMAL ATT', exc)
            ])
            )

df.to_csv('log_test_{}hours.txt'.format(hours_n), header=False, float_format='%+f', index=False)