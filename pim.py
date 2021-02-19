#!/usr/bin/env python3

import csv
import datetime
import os
from argparse import ArgumentParser
from os import system as sh

############################################################
# Parameter
############################################################

NDATES_GANTT = 20 # Number of dates to show in gannt chart

############################################################
# Color (ANSI escape sequence)
############################################################
ENDC           = '\033[0m'
BOLD           = '\033[1m'
UNDERLINE      = '\033[4m'

RED            = '\033[91m'
GREEN          = '\033[32m'
YELLOW         = '\033[33m'
BLUE           = '\033[34m'
MAGENTA        = '\033[35m'
CYAN           = '\033[36m'

BRIGHT_RED     = '\033[91m'
BRIGHT_GREEN   = '\033[92m'
BRIGHT_YELLOW  = '\033[93m'
BRIGHT_BLUE    = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN    = '\033[96m'


############################################################
# Method
############################################################
def print_items(lst):
    for item in lst:
        print('{} - {} ({}) : {}'.format(item[0], item[1], item[2], item[3]))
        # print('{0} - {1} :{4:<40} ({2}) : {3}'.format(item[0], item[1], item[2], item[3], item[4]))


def format_timediff1(timediff):
    hour = timediff.seconds // 3600
    minute = (timediff.seconds - hour * 3600) // 60
    return "{:0>2}:{:0>2}".format(hour, minute)


def format_timediff2(timediff):
    return "{} days".format(timediff.days)


def format_timediff3(timediff):
    return RED + "started" + ENDC

def print_col(str_, color):
    print(color + str_ + ENDC)

############################################################
# Main
############################################################
parser = ArgumentParser()
parser.add_argument('-f', '--future', action='store_true', help='show future schedule')
parser.add_argument('-b', '--backward', action='store_true', help='show backward schedule')
parser.add_argument('-p', '--project', action='store_true', help='show project list')
parser.add_argument('-g', '--gantt', action='store_true', help='show gantt chart')
parser.add_argument('-a', '--add', action='store_true', help='add schedule')
parser.add_argument('-q', '--queue', action='store_true', help='show job queue')
parser.add_argument('-e', '--edit', action='store_true', help='edit project file')
args = parser.parse_args()

now = datetime.datetime.now()
now_date = now.date()
oneday = datetime.timedelta(days=1)
tomo_date = now_date + oneday

format_long = '%Y-%m-%d %H:%M'
format_short = '%H:%M'
format_ymd = '%Y-%m-%d'

dir_script = os.path.dirname(__file__)
if dir_script == "":
    dir_script = "."

# print('It\'s {}'.format(now.strftime(format_long)))

#-----------------------------------------------------------
# Read schedule file
#-----------------------------------------------------------
list_today = []
list_future = []
list_backward = []
for line in csv.reader(open(dir_script + '/sche.csv')):
    datetime_sta = datetime.datetime.strptime(line[0], format_long)
    datetime_end = datetime.datetime.strptime(line[1], format_long)
    datetime_diff = datetime_sta - now
    name = line[2]
    delta1 = datetime_sta - datetime.datetime(now.year, now.month, now.day)
    delta2 = datetime_end - datetime_sta
    gantt = ''
    for _ in range(delta1.days):
        gantt += ' '
    for _ in range(delta2.days + 1):
        gantt += '*'

    # append "Today" list
    if (now_date <= datetime_sta.date() and
            datetime_end.date() < tomo_date):  # if today
        if now < datetime_end:  # not finished
            if datetime_sta <= now:  # started yet
                list_today.append([datetime_sta.strftime(format_short),
                                   datetime_end.strftime(format_short),
                                   format_timediff3(datetime_diff),
                                   name])
            else:  # not started
                list_today.append([datetime_sta.strftime(format_short),
                                   datetime_end.strftime(format_short),
                                   format_timediff1(datetime_diff),
                                   name])
    # append "Future" list
    if tomo_date <= datetime_sta.date():
        list_future.append([datetime_sta.strftime(format_long),
                            datetime_end.strftime(format_long),
                            format_timediff2(datetime_diff),
                            name])
    # append "Past" list
    if datetime_end.date() < now_date:
        list_backward.append([datetime_sta.strftime(format_long),
                              datetime_end.strftime(format_long),
                              format_timediff2(datetime_diff),
                              name])

#-----------------------------------------------------------
# Read project file
#-----------------------------------------------------------
lst_queue = []
str_run = ""
for index, line in enumerate(csv.reader(open(dir_script + '/proj.csv'))):
    if line[3] == "QUE":
        if len(line) != 5:
            if len(line) == 6:
                i = 5
            elif len(line) == 7:
                i = 6
            datetime_sta = datetime.datetime.strptime(line[5], format_ymd)
            datetime_end = datetime.datetime.strptime(line[i], format_ymd) + datetime.timedelta(days=1)
            if now < datetime_sta or datetime_end < now:
                continue
        lst_queue.append(["{:3d} {:3} : {} : {}".format(index+1, line[0], line[1], line[2]), int(line[4])])
    elif line[3] == "RUN":
        str_run = ["{:3d} {:3} : {} : {}".format(index+1, line[0], line[1], line[2]), int(line[4])]
lst_queue.reverse()
lst_queue.sort(key=lambda x: x[1])
# print(lst_queue)

#-----------------------------------------------------------
# Read time table file
#-----------------------------------------------------------
lst_ttable = []
for line in csv.reader(open(dir_script + '/ttable.csv')):
    lst_ttable.append(line)

#-----------------------------------------------------------
# Read holiday file
#-----------------------------------------------------------
lst_holiday = []
for index, line in enumerate(csv.reader(open(dir_script + '/syukujitsu.csv'))):
    if index == 0:
        continue
    lst_holiday.append(datetime.datetime.strptime(line[0], "%Y/%m/%d").date())

#-----------------------------------------------------------
# Read nenkyu file
#-----------------------------------------------------------
lst_nenkyu = []
for index, line in enumerate(csv.reader(open(dir_script + '/nenkyu.csv'))):
    lst_nenkyu.append(datetime.datetime.strptime(line[0], "%Y/%m/%d").date())

#-----------------------------------------------------------
# Show result
#-----------------------------------------------------------
try:
    has_opt = False
    if args.future:
        print_items(list_future)
        has_opt = True
    if args.backward:
        print_items(list_backward)
        has_opt = True
    if args.project:
        print("{:3} {:3} {:3} {}".format(UNDERLINE + 'IND' + ENDC, UNDERLINE + 'PRI' + ENDC, UNDERLINE + 'STA' + ENDC, UNDERLINE + 'TASK' + ENDC))
        for index, line in enumerate(csv.reader(open(dir_script + '/proj.csv'))):
            if line[3] == "QUE":
                print("{:3d} {:3d} {:3} {} : {} : {}".format(index + 1, int(line[4]), GREEN  + line[3] + ENDC, line[0], line[1], line[2]))
            elif line[3] == "RUN":
                print("{:3d} {:3d} {:3} {} : {} : {}".format(index + 1, int(line[4]), RED    + line[3] + ENDC, line[0], line[1], line[2]))
            elif line[3] == "PEN":
                print("{:3d} {:3d} {:3} {} : {} : {}".format(index + 1, int(line[4]), YELLOW + line[3] + ENDC, line[0], line[1], line[2]))
            elif line[3] == "HLD":
                print("{:3d} {:3d} {:3} {} : {} : {}".format(index + 1, int(line[4]), BLUE   + line[3] + ENDC, line[0], line[1], line[2]))
            elif line[3] == "FIN":
                pass
            else:
                print("{:3d} {:3d} {:3} {} : {} : {}".format(index + 1, int(line[4]), line[3]                , line[0], line[1], line[2]))
        has_opt = True
    if args.gantt:
        print("{:3} {:3} {:3} {}".format(UNDERLINE + 'IND' + ENDC, UNDERLINE + 'PRI' + ENDC, UNDERLINE + 'STA' + ENDC, UNDERLINE + 'TASK' + ENDC))
        for index, line in enumerate(csv.reader(open(dir_script + '/proj.csv'))):
            if line[3] == "QUE":
                print("{:3d} {:3d} {:3} {} : {} : {}".format(index + 1, int(line[4]), GREEN  + line[3] + ENDC, line[0], line[1], line[2]))
            elif line[3] == "RUN":
                print("{:3d} {:3d} {:3} {} : {} : {}".format(index + 1, int(line[4]), RED    + line[3] + ENDC, line[0], line[1], line[2]))
            elif line[3] == "PEN":
                print("{:3d} {:3d} {:3} {} : {} : {}".format(index + 1, int(line[4]), YELLOW + line[3] + ENDC, line[0], line[1], line[2]))
            elif line[3] == "HLD":
                print("{:3d} {:3d} {:3} {} : {} : {}".format(index + 1, int(line[4]), BLUE   + line[3] + ENDC, line[0], line[1], line[2]))
            elif line[3] == "FIN":
                pass
            else:
                print("{:3d} {:3d} {:3} {} : {} : {}".format(index + 1, int(line[4]), line[3]                , line[0], line[1], line[2]))
        print('')
        # print('           ', end='')
        print('                 ', end='')
        for index, line in enumerate(csv.reader(open(dir_script + '/proj.csv'))):
            if line[3] != "FIN":
                print('{:2d}'.format(index+1), end=' ')
        print('')
        cur_date = now_date
        for i in range(NDATES_GANTT):
            dow = cur_date.strftime('%a')
            if dow == 'Sat':
                print(cur_date.strftime('%Y-%m-%d ({}{}{})'.format(CYAN, dow, ENDC)), end=' ')
            elif dow == 'Sun':
                print(cur_date.strftime('%Y-%m-%d ({}{}{})'.format(RED, dow, ENDC)), end=' ')
            else:
                if cur_date in lst_holiday or cur_date in lst_nenkyu:
                    print(cur_date.strftime('%Y-%m-%d ({}{}{})'.format(RED, dow, ENDC)), end=' ')
                else:
                    print(cur_date.strftime('%Y-%m-%d ({})'.format(dow)), end=' ')
            for index, line in enumerate(csv.reader(open(dir_script + '/proj.csv'))):
                if line[3] != "FIN":
                    if len(line) == 6:
                        datetime_sta = datetime.datetime.strptime(line[5], format_ymd)
                        datetime_end = datetime.datetime.strptime(line[5], format_ymd)
                    elif len(line) == 7:
                        datetime_sta = datetime.datetime.strptime(line[5], format_ymd)
                        datetime_end = datetime.datetime.strptime(line[6], format_ymd)
                    else:
                        datetime_sta = None
                        datetime_end = None
                    if datetime_sta is None:
                        print('  ', end=' ')
                    elif datetime_sta.date() <= cur_date and cur_date < datetime_end.date() + oneday:
                        print(' *', end=' ')
                    else:
                        print('  ', end=' ')
            cur_date = cur_date + oneday
            print('')
        has_opt = True
    if args.queue:
        i = 0
        print("{:4} {:3} {:}".format(UNDERLINE + 'TIME' + ENDC + ' ' * 9, UNDERLINE + 'IND' + ENDC, UNDERLINE + 'TASK' + ENDC))
        for titem in lst_ttable:
            dt_tmp1 = datetime.datetime(now.year, now.month, now.day, int(titem[0].split(":")[0]), int(titem[0].split(":")[1]))
            dt_tmp2 = datetime.datetime(now.year, now.month, now.day, int(titem[1].split(":")[0]), int(titem[1].split(":")[1]))
            if now < dt_tmp2: # Show term which is not finished.
                if titem[2] != "":
                    lst_tmp = []
                    while len(lst_queue) != 0:
                        qitem = lst_queue.pop()
                        if titem[2] in qitem[0].split('：')[0]:
                            # print("{} - {}: {}".format(titem[0], titem[1], lst_queue[i][0]))
                            print("{} - {} {}".format(titem[0], titem[1], qitem[0]))
                            break
                        lst_tmp.append(qitem)
                    lst_tmp.reverse()
                    lst_queue = lst_queue + lst_tmp
                else:
                    qitem = lst_queue.pop()
                    # print("{} - {}: {}".format(titem[0], titem[1], lst_queue[i][0]))
                    print("{} - {} {}".format(titem[0], titem[1], qitem[0]))
                # if dt_tmp1 <= now and now < dt_tmp2:
                    # if str_run != "":
                        # print("{} - {}: {}".format(titem[0], titem[1], str_run[0]))
                # elif now <= dt_tmp1:
                    # print("{} - {}: {}".format(titem[0], titem[1], lst_queue[i][0]))
                    # i += 1
                i += 1
        has_opt = True
    if args.add:
        add_start = input("start date -> ")
        add_end = input("end date -> ")
        if add_start == "" and add_end == "":
            add_start = now
            add_end = now + oneday
        add_title = input("title -> ")
        f = open(dir_script + '/sche.csv', "a")
        f.write(add_start.strftime("%Y-%m-%d %H:%M") + ',' + add_end.strftime("%Y-%m-%d %H:%M") + ',' + add_title + "\n")
        f.close()
        has_opt = True
    if args.edit:
        sh('vim {0}/proj.csv {0}/ttable.csv'.format(os.path.dirname(__file__)))
        has_opt = True
    if not has_opt:
        print_items(list_today)
except Exception as e:
    print(RED + "*** Error occured in parsing csv file! ***" + ENDC)
    print(e)
    print(line)
