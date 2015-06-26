#!/usr/bin/env python

import datetime
import csv
import os

now = datetime.datetime.now()
now_date = now.date()
tomo_date = now_date + datetime.timedelta(days=1)

format_long = '%Y-%m-%d %H:%M'
format_short = '%H:%M'

dir_script = os.path.dirname(__file__)

#print 'It\'s {}'.format(now.strftime(format_long))

list_today = []
list_sche = []
for line in csv.reader(open(dir_script + '/sche.csv')):
    datetime_sta = datetime. datetime.strptime(line[0], format_long)
    datetime_end = datetime. datetime.strptime(line[1], format_long)
    datetime_diff = datetime_sta - now
    name = line[2]
    # append "Today" list
    if(now_date <= datetime_sta.date() and 
            datetime_end.date() < tomo_date): # if today
        if(now < datetime_end):
            list_today.append([datetime_sta.strftime(format_short),
                datetime_end.strftime(format_short),
                datetime_diff,
                name])
    # append "Schedule" list
    if(tomo_date <= datetime_sta.date()):
        list_sche.append([datetime_sta.strftime(format_long),
            datetime_end.strftime(format_long),
            datetime_diff,
            name])

for item in list_today:
    print '{} - {} ({}) : {}'.format(item[0], item[1], item[2], item[3])

print ''

print 'Schedule'
for item in list_sche:
    print '{} - {} ({}) : {}'.format(item[0], item[1], item[2], item[3])
