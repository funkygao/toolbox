#!/usr/bin/env python
#encoding=utf-8

import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import json
import locale as syslocale
import matplotlib.ticker as tkr

FIG_TITLE_FONT_SIZE = 18
COLORS = ['b', 'r', 'g', 'y', 'm', 'c']

def save_figure(fig, name):
    filename = 'chart/' + name + '.jpg'
    fig.gca().hold(False)
    fig.savefig(filename, dpi=150)

def call_php_fetch():
    from subprocess import call
    call(['php', 'fetch.php'])

def commas_func(x, pos):  # formatter function takes tick label and tick position
   return '{:0,d}'.format(int(x))

def commas_thousand(i):
    ''' commas_thousand(12453) -> '12,453'
    '''
    return syslocale.format("%d", i, grouping=True)

def load_days(category, locale='us'):
    '''load the x axis series'''
    with open('var/' + locale + '_' + category + 'Days') as f:
        days = json.loads(f.readlines()[0])
    return ['-'.join(d.split('-')[1:]) for d in days]

def draw_lines(locales, metrics, title, numRows, numCols, target, grid = True, show_result = False, days = 'dau'):
    '''metrics = [('arpu', 'ARPU'), ('arppu', 'ARPPU')]
    '''
    days = load_days(days)
    datas = [[] for x in range(len(metrics))] # datas[plot][locale][day]
    for locale in locales:
        for i, metric in enumerate(metrics):
            data_file = 'var/' + locale + '_' + metric[0]
            with open(data_file) as f:
                js = json.loads(f.readlines()[0])
                datas[i].append(js[0]['data'])
    
    # start to draw
    fig = pl.figure()
    fig.suptitle(title, fontsize=FIG_TITLE_FONT_SIZE)
    plots = []
    for i, _ in enumerate(metrics):
        plot= plt.subplot(100 * numRows + 10 * numCols + i + 1)
        plot.grid(grid)
        plots.append(plot)

    for locale_idx, _ in enumerate(locales):
        for plot_idx, plot in enumerate(plots):
            plt.sca(plot)
            pl.plot(datas[plot_idx][locale_idx][:len(days)], label = locales[locale_idx])

    for i, plot in enumerate(plots):
        plt.sca(plot)
        pl.title(metrics[i][1])
        pl.legend(loc = 'lower left')
        pl.xticks(range(len(days)), days)
        pl.xlabel(u'日期')
        #pl.ylabel(ylabel)

    if show_result:
        pl.show()

    save_figure(fig, target)

    if show_result:
        pl.show()

def draw_stacked_bars(locales, metric, title, target, grid = True, show_result = False, days = 'dau', width=0.35):
    days = load_days(days)
    datas = []
    for locale in locales:
        data_file = 'var/' + locale + '_' + metric
        with open(data_file) as f:
                js = json.loads(f.readlines()[0])
                datas.append(np.add(js[1]['data'], js[0]['data'])) # sum of the 2 numbers

    # start to draw
    fig = pl.figure()
    fig.suptitle(title, fontsize=FIG_TITLE_FONT_SIZE)
    ax = plt.subplot(111)
    ax.grid(grid)

    bars = []
    bottom = [0.0 for d in range(len(days))]
    for i, y in enumerate(datas):
        if i != 0:
            bottom = np.add(bottom, datas[i-1][:len(days)])
        bar = plt.bar(range(len(days)), y[:len(days)], color=COLORS[i], bottom=bottom, width=width, label=locales[i])
        xs = [mm.get_x() for mm in bar]
        ys = np.add(bottom, y[:len(days)])
        bars.append(bar)

    # draw the text on each bar top
    for i, x in enumerate(xs):
        plt.text(x, 1.01 * ys[i], commas_func(ys[i], 3))

    plt.legend((b[0] for b in bars), locales)
    pl.xticks(np.arange(len(days)) + width/2., days)
    y_format = tkr.FuncFormatter(commas_func)
    ax.yaxis.set_major_formatter(y_format) # set formatter to needed axis

    if show_result:
        pl.show()

    save_figure(fig, target)

def get_locales(file='var/locales'):
    with open(file) as f:
        return json.loads(f.readlines()[0])
    return None

def init():
    from pylab import rcParams
    rcParams['figure.figsize'] = 18, 11
    syslocale.setlocale(syslocale.LC_ALL, 'en_US')

def draw_arpu(locales):
    draw_stacked_bars(locales, 'paymentDatas', 'arpu vs arppu', 'arpu1', grid = True, days = 'dau')

if __name__ == '__main__':
    init()
    locales = get_locales()
    draw_stacked_bars(locales, 'paymentDatas', 'Payments', 'paystacked', grid = True, days = 'dau')
    draw_arpu(locales)
