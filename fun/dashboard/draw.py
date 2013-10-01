#!/usr/bin/env python
#encoding=utf-8
''' TODO
plt.bar(bottom=xxx) to stack bar http://matplotlib.org/examples/pylab_examples/table_demo.html
'''

import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import json
import sys
import locale as syslocale
from plot import *

FIG_TITLE_FONT_SIZE = 20

show_result = False

def draw_arpu(locales):
    # prepare data
    arpus, arppus, labels = [], [], [] # labels for legend
    days = load_days('dau')
    for locale in locales:
        file = 'var/' + locale + '_ARPU'
        with open(file) as f:
            datas = json.loads(f.readlines()[0])
            arpus.append(datas[0]['data'])
            labels.append(locale)

        file = 'var/' + locale + '_ARPPU'
        with open(file) as f:
            datas = json.loads(f.readlines()[0])
            arppus.append(datas[0]['data'])

    # start to draw
    fig = pl.figure()
    fig.suptitle('ARPU - ARPPU', fontsize=FIG_TITLE_FONT_SIZE)
    ax1 = plt.subplot(121) # numRows, numCols, plotNum
    ax1.grid(True)
    ax2 = plt.subplot(122)
    ax2.grid(True)
    for i, y in enumerate(arpus): # new users in each locale
        plt.sca(ax1) 
        pl.plot(y[:len(days)], label=labels[i])

        plt.sca(ax2)
        pl.plot(arppus[i][:len(days)], label=labels[i])

    setup_fig(ax1, u'ARPU', range(len(days)), days, u'日期', u'金额')
    setup_fig(ax2, u'ARPPU', range(len(days)), days, u'日期', u'金额')
    save_figure(fig, 'arpu')

    if show_result:
        pl.show()

def draw_revenue(locales):
    # prepare data
    new_users, old_users, labels = [], [], []
    days = load_days('dau')
    for locale in locales:
        # y axis, new/old users
        file = 'var/' + locale + '_paymentDatas'
        with open(file) as f:
            datas = json.loads(f.readlines()[0])
            new_users.append(datas[0]['data'])
            old_users.append(datas[1]['data'])
            labels.append(locale)

    # start to draw
    fig = pl.figure()
    plt.grid(True)
    fig.suptitle('Revenue', fontsize=FIG_TITLE_FONT_SIZE)
    ax1 = plt.subplot(311) # numRows, numCols, plotNum
    ax1.grid(True)
    ax2 = plt.subplot(312)
    ax2.grid(True)
    ax3 = plt.subplot(313)
    ax3.grid(True)
    for i, y in enumerate(new_users): # new users in each locale
        plt.sca(ax2) 
        pl.plot(y[:len(days)], label=labels[i])

        plt.sca(ax1)
        pl.plot(np.add(y[:len(days)], old_users[i][:len(days)]), label=labels[i])

        plt.sca(ax3)
        pl.plot(np.multiply(100, np.divide(np.double(new_users[i][:len(days)]), np.add(new_users[i][:len(days)], old_users[i][:len(days)]))), label=labels[i])

    setup_fig(ax1, u'总支付', range(len(days)), days, u'日期', u'金额')
    setup_fig(ax2, u'首次支付', range(len(days)), days, u'日期', u'金额')
    setup_fig(ax3, u'首次支付占比', range(len(days)), days, u'日期', u'%')
    save_figure(fig, 'revenue')

    if show_result:
        pl.show()

def draw_dau(locales):
    # prepare data
    new_users, old_users, labels = [], [], []
    days = load_days('dau')
    for locale in locales:
        # y axis, new/old users
        file = 'var/' + locale + '_dauDatas'
        with open(file) as f:
            datas = json.loads(f.readlines()[0])
            new_users.append(datas[0]['data'])
            old_users.append(datas[1]['data'])
            labels.append(locale)

    # start to draw
    fig = pl.figure()
    fig.suptitle('DAU', fontsize=FIG_TITLE_FONT_SIZE)
    ax1 = plt.subplot(131) # numRows, numCols, plotNum
    ax1.grid(True)
    ax2 = plt.subplot(132)
    ax2.grid(True)
    ax3 = plt.subplot(133)
    ax3.grid(True)
    for i, y in enumerate(new_users): # new users in each locale
        plt.sca(ax2) 
        pl.plot(y[:len(days)], label=labels[i]) # different locales data may come in disorder

        plt.sca(ax1)
        pl.plot(np.add(y[:len(days)], old_users[i][:len(days)]), label=labels[i])

        plt.sca(ax3)
        pl.plot(np.multiply(100, np.divide(np.double(new_users[i][:len(days)]), np.add(new_users[i][:len(days)], old_users[i][:len(days)]))), label=labels[i])

    setup_fig(ax1, u'总玩家', range(len(days)), days, 'date', 'num')
    setup_fig(ax2, u'新用户', range(len(days)), days, 'date', 'num')
    setup_fig(ax3, u'新玩家占总玩家比率', range(len(days)), days, 'date', '%')
    save_figure(fig, 'dau')

    if show_result:
        pl.show()

def draw_retention(locales):
    # prepare data
    retentions2, retentions3, retentions7, labels = [], [], [], []
    days = load_days('retention')
    for locale in locales:
        # y axis, new/old users
        file = 'var/' + locale + '_retentionDatas'
        with open(file) as f:
            datas = json.loads(f.readlines()[0])
            retentions2.append(datas[0]['data'])
            retentions3.append(datas[1]['data'])
            retentions7.append(datas[2]['data'])
            labels.append(locale)

    # start to draw
    fig = pl.figure()
    fig.suptitle('Rentention', fontsize=FIG_TITLE_FONT_SIZE)
    ax1 = plt.subplot(311) # numRows, numCols, plotNum
    ax1.grid(True)
    ax2 = plt.subplot(312)
    ax2.grid(True)
    ax3 = plt.subplot(313)
    ax3.grid(True)
    for i, y in enumerate(retentions2): # new users in each locale
        plt.sca(ax1) 
        pl.plot(y[:len(days)], label=labels[i])

        plt.sca(ax2)
        pl.plot(retentions3[i][:len(days)], label=labels[i])

        plt.sca(ax3)
        pl.plot(retentions7[i][:len(days)], label=labels[i])

    setup_fig(ax1, u'2日留存率', range(len(days)), days, 'date', '%')
    setup_fig(ax2, u'3日留存率', range(len(days)), days, 'date', '%')
    setup_fig(ax3, u'7日留存率', range(len(days)), days, 'date', '%')
    save_figure(fig, 'retention')

    if show_result:
        pl.show()

def draw_dau_vs_revenue(locales):
    # prepare data
    daus_labels, payments_labels = [], []
    new_users, old_users = [], []
    new_pay, old_pay = [], []
    days = load_days('dau')
    for locale in locales:
        file = 'var/' + locale + '_dauDatas'
        with open(file) as f:
            datas = json.loads(f.readlines()[0])
            new_users.append(datas[0]['data'])
            old_users.append(datas[1]['data'])
            daus_labels.append(locale + '_dau')

        file = 'var/' + locale + '_paymentDatas'
        with open(file) as f:
            datas = json.loads(f.readlines()[0])
            new_pay.append(datas[0]['data'])
            old_pay.append(datas[1]['data'])
            payments_labels.append(locale + '_$')

    # start to draw
    fig = pl.figure()
    fig.suptitle(u'总玩家 vs 总支付(左人数，右钱数)', fontsize=FIG_TITLE_FONT_SIZE)
    ax1 = plt.subplot(111) # numRows, numCols, plotNum
    ax2 = ax1.twinx()
    for i, y in enumerate(new_users): # new users in each locale
        plt.sca(ax1) 
        pl.plot(np.add(new_users[i][:len(days)], old_users[i][:len(days)]) , label=daus_labels[i])

        plt.sca(ax2)
        pl.plot(np.add(new_pay[i][:len(days)], old_pay[i][:len(days)]) , '*:', label=payments_labels[i])

    setup_fig(ax1, u' ', range(len(days)), days, 'date', 'num')
    setup_fig(ax2, u' ', range(len(days)), days, 'money', 'num')
    ax1.set_ylabel(u'DAU人数')
    ax2.set_ylabel(u'金额')
    plt.sca(ax1)
    pl.legend(loc = 'lower left')
    plt.sca(ax2)
    pl.legend(loc = 'lower right')
    save_figure(fig, 'dauVsRevenue')

    if show_result:
        pl.show()

def draw_retention_vs_arpu(locales):
    # prepare data
    retentions2, arpus, retention_labels, arpu_labels = [], [], [], []
    days = load_days('retention')
    for locale in locales:
        file = 'var/' + locale + '_retentionDatas'
        with open(file) as f:
            datas = json.loads(f.readlines()[0])
            retentions2.append(datas[0]['data'])
            retention_labels.append(locale + "_r")
        
        file = 'var/' + locale + '_ARPU'
        with open(file) as f:
            datas = json.loads(f.readlines()[0])
            arpus.append(datas[0]['data'])
            arpu_labels.append(locale + "_a")

    # start to draw
    fig = pl.figure()
    fig.suptitle('Rentention 2 days vs ARPU', fontsize=FIG_TITLE_FONT_SIZE)
    ax1 = plt.subplot(111) # numRows, numCols, plotNum
    #ax1.grid(True)
    ax2 = ax1.twinx()
    #ax2.grid(True)
    for i, y in enumerate(retentions2): # new users in each locale
        plt.sca(ax1) 
        pl.plot(arpus[i][:len(days)], label=arpu_labels[i])

        plt.sca(ax2)
        pl.plot(retentions2[i][:len(days)], '*:', label=retention_labels[i])

    ax1.set_ylabel(u'金额')
    ax2.set_ylabel(u'2日留存率%')
    plt.sca(ax1)
    pl.legend(loc = 'lower left')
    plt.sca(ax2)
    pl.legend(loc = 'lower right')
    save_figure(fig, 'retentionVsArpu')

    if show_result:
        pl.show()

def draw_stacked_revenue(locales):
    draw_stacked_bars(locales, 'paymentDatas', 'Daily Total Revenue', 'stacked_revenue', grid = True, days = 'dau')

def draw_stacked_dau(locales):
    draw_stacked_bars(locales, 'dauDatas', 'Daily Total DAU', 'stacked_dau', grid = True, days = 'dau')

def setup_fig(ax, title, xticks1, xticks2, xlabel, ylabel):
    plt.sca(ax)
    pl.title(title)
    pl.legend(loc = 'lower left')
    pl.xticks(xticks1, xticks2)
    pl.xlabel(xlabel)
    pl.ylabel(ylabel)
    y_format = tkr.FuncFormatter(commas_func)
    ax.yaxis.set_major_formatter(y_format)

def write_finish_time(target):
    from time import ctime
    with open(target, 'w') as f:
        f.write(ctime())

def main():
    init()

    for arg in sys.argv:
        if arg == 'show':
            global show_result
            show_result = True
        elif arg == 'init':
            call_php_fetch()

    locales = get_locales()
    if locales is None:
        sys.Exit(1)

    draw_dau(locales)
    draw_arpu(locales)
    draw_revenue(locales)
    draw_retention(locales)
    draw_retention_vs_arpu(locales)
    draw_dau_vs_revenue(locales)
    draw_stacked_revenue(locales)
    draw_stacked_dau(locales)
    write_finish_time('var/done.txt')

if __name__ == '__main__':
    main()
