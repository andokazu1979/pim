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
tdelta_rest_in_sec = 0

while dt < datetime.datetime(dt_now.year, dt_now.month, dt_now.day, 20, 30):
    dt2 = dt + datetime.timedelta(hours=1)
    print('{0},{1},'.format(dt.strftime("%H:%M"), dt2.strftime("%H:%M")))
    dt += datetime.timedelta(seconds=(3600+tdelta_rest_in_sec))
