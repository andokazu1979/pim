#!/usr/bin/env python

import datetime
import csv
import os
from argparse import ArgumentParser

############################################################
# Method
############################################################
def print_items(list):
    for item in list:
        print '{} - {} ({}) : {}'.format(item[0], item[1], item[2], item[3])

############################################################
# Main
############################################################
parser = ArgumentParser()
parser.add_argument('-f', '--future', action = 'store_true', help = 'show future schedule')
parser.add_argument('-b', '--backward', action = 'store_true', help = 'show backward schedule')
args = parser.parse_args()

now = datetime.datetime.now()
now_date = now.date()
tomo_date = now_date + datetime.timedelta(days=1)

format_long = '%Y-%m-%d %H:%M'
format_short = '%H:%M'

dir_script = os.path.dirname(__file__)

#print 'It\'s {}'.format(now.strftime(format_long))

list_today = []
list_future = []
list_backward = []
for line in csv.reader(open(dir_script + '/sche.csv')):
    datetime_sta = datetime. datetime.strptime(line[0], format_long)
    datetime_end = datetime. datetime.strptime(line[1], format_long)
    datetime_diff = datetime_sta - now
    name = line[2]
    # append "Today" list
    if(now_date <= datetime_sta.date() and 
            datetime_end.date() < tomo_date): # if today
        if(now < datetime_end): # not finished
            list_today.append([datetime_sta.strftime(format_short),
                datetime_end.strftime(format_short),
                datetime_diff,
                name])
    # append "Future" list
    if(tomo_date <= datetime_sta.date()):
        list_future.append([datetime_sta.strftime(format_long),
            datetime_end.strftime(format_long),
            datetime_diff,
            name])
    # append "Past" list
    if(datetime_end.date() < tomo_date):
        list_backward.append([datetime_sta.strftime(format_long),
            datetime_end.strftime(format_long),
            datetime_diff,
            name])

has_opt = False
if(args.future):
    print_items(list_future)
    has_opt = True
if(args.backward):
    print_items(list_backward)
    has_opt = True
if(not has_opt):
    print_items(list_today)

    
