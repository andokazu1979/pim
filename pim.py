#!/usr/bin/env python

import datetime
import csv
import os
from argparse import ArgumentParser

############################################################
# Color (ANSI escape sequence)
############################################################
PURPLE = '\033[95m'
OKBLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

############################################################
# Method
############################################################
def print_items(list):
    for item in list:
        print '{} - {} ({}) : {}'.format(item[0], item[1], item[2], item[3])

def format_timediff1(timediff):
    hour = timediff.seconds // 3600
    minute = (timediff.seconds - hour * 3600) // 60
    return "{:0>2}:{:0>2}".format(hour, minute)

def format_timediff2(timediff):
    return "{} days".format(timediff.days)

def format_timediff3(timediff):
    return "started"

############################################################
# Main
############################################################
parser = ArgumentParser()
parser.add_argument('-f', '--future', action = 'store_true', help = 'show future schedule')
parser.add_argument('-b', '--backward', action = 'store_true', help = 'show backward schedule')
parser.add_argument('-p', '--project', action = 'store_true', help = 'show project list')
parser.add_argument('-a', '--add', action = 'store_true', help = 'add schedule')
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
            if(datetime_sta <= now): # started yet
                list_today.append([datetime_sta.strftime(format_short),
                    datetime_end.strftime(format_short),
                    format_timediff3(datetime_diff),
                    name])
            else: # not started
                list_today.append([datetime_sta.strftime(format_short),
                    datetime_end.strftime(format_short),
                    format_timediff1(datetime_diff),
                    name])
    # append "Future" list
    if(tomo_date <= datetime_sta.date()):
        list_future.append([datetime_sta.strftime(format_long),
            datetime_end.strftime(format_long),
            format_timediff2(datetime_diff),
            name])
    # append "Past" list
    if(datetime_end.date() < now_date):
        list_backward.append([datetime_sta.strftime(format_long),
            datetime_end.strftime(format_long),
            format_timediff2(datetime_diff),
            name])

has_opt = False
if(args.future):
    print_items(list_future)
    has_opt = True
if(args.backward):
    print_items(list_backward)
    has_opt = True
if(args.project):
    for line in csv.reader(open(dir_script + '/proj.csv')):
        if(line[2] == "PEND"):
            print "{} : {} ({})".format(line[0], line[1], GREEN+line[2]+ENDC)
        elif(line[2] == "RUN"):
            print "{} : {} ({})".format(line[0], line[1], RED+line[2]+ENDC)
        else:
            print "{} : {} ({})".format(line[0], line[1], line[2])
    has_opt = True
if(args.add):
    add_start = raw_input("start date -> ")
    add_end = raw_input("end date -> ")
    add_title = raw_input("title -> ")
    f = open(dir_script + '/sche.csv', "a")
    f.write(add_start + ',' + add_end + ',' + add_title)
    f.close()
    has_opt = True
if(not has_opt):
    print_items(list_today)

    
