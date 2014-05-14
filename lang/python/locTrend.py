#!/usr/bin/env python
'''show trends of LineOfCode by weeks
'''

import sys
import subprocess
import collections
from datetime import datetime, timedelta

#==============
# configurables
#==============
REPO_BASEDIR = '../'  # VERY important, what base repo dir are you tracking
YEAR_N = 1                       # how long ago are you tracking
MONTH_IN_YEAR = 52
GIT_CMD = 'git log --shortstat --since "%d weeks ago" --until "%d week ago" %s| grep "files\? changed"'

def date_of_weeks_ago(weeks_ago):
    '''first date of some weeks ago'''
    date = (datetime.now() - timedelta(weeks=weeks_ago)).date()
    return '%d-%d' % (date.month, date.day)

def net_added_lines_of_week(week):
    ''' -> added_loc, deleted_loc'''
    deleted_loc = 0
    added_loc =0
    lines = subprocess.Popen(GIT_CMD % (week+1, week, REPO_BASEDIR), shell=True, stdout=subprocess.PIPE).stdout.readlines()
    for line in lines:
        line = line.strip()
        parts = line.split(' ')
        if len(parts) == 5:
            # only insert or delete
            if parts[4].startswith('dele'):
                deleted_loc += int(parts[3])
            elif parts[4].startswith('inser'):
                added_loc += int(parts[3])
            else:
                print 'unrecognized line:', line
                sys.exit(1)
        elif len(parts) == 7:
            # both insert and delete
            added_loc += int(parts[3])
            deleted_loc += int(parts[5])
   
    return added_loc, deleted_loc
    
def show_trend_csv(stats):
    '''show in csv format'''
    print
    print '*' * 20
    print 'In csv format'
    print '*' * 20
    net_lines = 0
    print 'week_start_date,net_loc'
    for stat in stats.items():
        weeks_ago, added, deleted = stat[0], stat[1]['add'], stat[1]['del']
        net_lines += added - deleted
        if net_lines == 0:
            continue
        print '%s,%d' % (date_of_weeks_ago(weeks_ago), net_lines)

def show_trand_chart(stats):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        sys.exit(0)

    # prepare data
    net_lines = 0
    xlabels, axisx, axisy = [], [], []
    for stat in stats.items():
        weeks_ago, added, deleted = stat[0], stat[1]['add'], stat[1]['del']
        net_lines += added - deleted
        if net_lines == 0:
            continue

        xlabels.append(date_of_weeks_ago(weeks_ago))
        axisx.append(weeks_ago)
        axisy.append(net_lines)

    # start to plot
    plt.locator_params(axis = 'x', nbins = 4)
    plt.grid(True)
    plt.xlabel('weeks ago')
    plt.ylabel('LoC')
    plt.title('LineOfCode trend')
    plt.xticks(axisx, xlabels)
    plt.plot(axisx, axisy)
    plt.show()

def run_loc_trend(year):
    '''The main entry'''
    stats={}
    for week in reversed(range(0, MONTH_IN_YEAR * year)): # weekly contributions for N years in reverse order
        lines_added, lines_deleted = net_added_lines_of_week(week)
        stats[week] = {}
        stats[week]['add'] = int(lines_added)
        stats[week]['del'] = int(lines_deleted)
    
    net_lines = 0
    print '='* 102
    print '=' * 30, 'LineOfCode trend over the past %d year(s)' % year, '=' * 30
    print '='* 102
    print '%12s %12s %12s %12s %12s' % ('weeksAgo', 'startDate', 'addedLines', 'deletedLines', 'netLines')
    stats_order_by_week_ago = collections.OrderedDict(sorted(stats.items(), reverse=True))
    for stat in stats_order_by_week_ago.items():
        weeks_ago, added, deleted = stat[0], stat[1]['add'], stat[1]['del']
        if added == 0 and deleted == 0:
            continue
        print '%12d %12s %12d %12d %12d' % (weeks_ago, date_of_weeks_ago(weeks_ago), added, deleted, added - deleted)
    
    
    #show_trend_csv(stats_order_by_week_ago)
    show_trand_chart(stats_order_by_week_ago)

if __name__ == '__main__':
    run_loc_trend(YEAR_N)

