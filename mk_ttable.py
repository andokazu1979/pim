#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime

time_sta = sys.argv[1]

dt_now = datetime.datetime.now()

tmp = time_sta.split(':')
hour = int(tmp[0])
minute = int(tmp[1])
dt = datetime.datetime(dt_now.year, dt_now.month, dt_now.day,  hour, minute)
tdelta_rest_in_min = 15
tdelta_rest_in_sec = tdelta_rest_in_min * 60

i = 0
while dt < datetime.datetime(dt_now.year, dt_now.month, dt_now.day, 20, 30):
    dt2 = dt + datetime.timedelta(seconds=1500)
    print('{0},{1},'.format(dt.strftime("%H:%M"), dt2.strftime("%H:%M")))
    if (i + 1) % 4 == 0:
        dt += datetime.timedelta(seconds=(1800+(tdelta_rest_in_sec - 300)))
    else:
        dt += datetime.timedelta(seconds=(1800))
    i += 1
