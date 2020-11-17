#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
from pathlib import PurePath
import accessory.colorprint as cp
import accessory.clear_consol as cc
import accessory.authorship as auth_sh
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import cm


IMAGESAVE = True
CLOSECONSOLE = True

# ==================================================================================================

def mouse_graph_report(filename, imagesave=True):
    points = filedata_read(filename)

    allx = [point[0] for point in points]
    ally = [point[1] for point in points]
    time_ = [point[2] for point in points]

    speedx = calculate_speed_axis(points, axis=0)
    speedy = calculate_speed_axis(points, axis=1)
    speed = calculate_speed(points)
    acceleration = calculate_acceleration(speed, time_)

    gradient = create_gradient(len(points))
    create_graphs(allx=allx, ally=ally,
                  speedx=speedx, speedy=speedy, speed=speed, acc=acceleration,
                  time_=time_, gradient=gradient, filename=filename, imagesave=imagesave)

def filedata_read(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as fr:
            str_arrey = fr.read().split('\n')
    except Exception as e:
       cp.cprint(f'4Ошибка чтения файла ^15_{filename}')
       # print(e.__class__)
       exit(1)
    points = []
    try:
        for s in str_arrey:
            dat = s.split(' ')
            points.append([
                        int(dat[0]),
                        int(dat[1]),
                        float(dat[2])
                        ])
    except Exception as e:
        cp.cprint(f'4Неправильные данные в файле ^15_{filename}')
        exit(1)
    return points

def create_gradient(count=1):
    # один фиксированный цвет
    # gradient = [0.430983, 0.808473, 0.346476, 1]
    # если числа 0...50, то использовать параметр не 'color' а 'c'
    # gradient = np.random.randint(0, 50, count)

    # gradient = cm.get_cmap('viridis', count).colors
    # gradient = cm.get_cmap('plasma', count).colors
    # gradient = cm.get_cmap('Oranges', count)(range(count))
    # gradient = cm.get_cmap('GnBu', count)(range(count))
    gradient = cm.get_cmap('winter', count)(range(count))
    # gradient = np.flipud(gradient)  # реверс цвета
    return(gradient)

def calculate_speed_axis(points, axis):
    speed = []
    ds = points[0][axis]
    dt = points[0][2]
    for point in points:
        s = abs(point[axis] - ds)
        ds = point[axis]
        t = point[2] - dt
        dt = point[2]
        # print('s t  ', s, t)
        try:
            sp = s / t
        except ZeroDivisionError:
            sp = 0
        speed.append(sp)
    return speed

def calculate_speed(points):
    # AB = √(xb - xa)2 + (yb - ya)2
    speed = []
    dsx = points[0][0]
    dsy = points[0][1]
    dt = points[0][2]
    for point in points:
        sx = point[0]
        sy = point[1]
        s = ((sx - dsx)**2 + (sy - dsy)**2)**0.5
        dsx = sx
        dsy = sy
        t = point[2] - dt
        dt = point[2]
        # print('s t  ', s, t)
        try:
            sp = s / t
        except ZeroDivisionError:
            sp = 0
        speed.append(sp)
    return speed

def calculate_acceleration(speed, time_):
    # a = (V - V0) / t
    acceleration = []
    for ind, t in enumerate(time_):
        if ind == 0:
            acceleration.append(0)
            continue
        try:
            acc = (speed[ind] - speed[ind-1]) / t
        except ZeroDivisionError:
            acc = speed[ind] - speed[ind-1]
        # except IndexError:
            # acc = 0
        acceleration.append(acc)
    # print(speed)
    # print(acceleration)
    return acceleration


def create_graphs(allx, ally,
                  speedx, speedy, speed, acc,
                  time_, gradient, filename, imagesave=True):
    fig = plt.figure(
                    figsize=(cm_to_inch(35), cm_to_inch(20)),
                    dpi=100,
                    facecolor='#EEEEEE'
                    )
    gridsize = (2, 2)
    ax_path1   = plt.subplot2grid(gridsize, (0, 0))  #, colspan=2, rowspan=2
    ax_acc     = plt.subplot2grid(gridsize, (1, 0))
    ax_speed   = plt.subplot2grid(gridsize, (0, 1))
    ax_speedxy = plt.subplot2grid(gridsize, (1, 1))

    # gridsize = (2, 3)
    # ax_path1  = plt.subplot2grid(gridsize, (0, 0))  #, colspan=2, rowspan=2
    # ax_speedx = plt.subplot2grid(gridsize, (0, 1))
    # ax_speed  = plt.subplot2grid(gridsize, (0, 2))
    # ax_path2  = plt.subplot2grid(gridsize, (1, 0))
    # ax_speedy = plt.subplot2grid(gridsize, (1, 1))
    # ax_acc    = plt.subplot2grid(gridsize, (1, 2))

    fig.canvas.set_window_title(f'Графики для файла  {PurePath(filename).name}')
    fig.suptitle(f'для файла:  {PurePath(filename).name}')
    fig.set_tight_layout(True)

    create_graph_path1(ax_path1, allx, ally, gradient=gradient)
    create_graph_speed(ax_speedxy, time_, data_y=speedx, data_y_ex=speedy, title='Скорость по осям', c='firebrick')
    # create_graph_path2(ax_path2, allx, ally)
    # create_graph_speed(ax_speedx, time_, data_y=speedx, title='Скорость по X', c='firebrick')
    # create_graph_speed(ax_speedy, time_, data_y=speedy, title='Скорость по Y', c='darkgreen')
    create_graph_speed(ax_speed, time_, data_y=speed, title='Скорость курсора')
    create_graph_speed(ax_acc, time_, data_y=acc,
                       title='Ускорение', ylabel='ускорение px/ms²',
                       c='hotpink', linewidth=1)
    # plt.yscale('log')

    plt.tight_layout()
    if imagesave:
        plt.savefig(f'{PurePath(filename).stem}.png')
    plt.show()
    plt.close()

def create_graph_path1(ax_path1, allx, ally, gradient=None):
    ax_path1.scatter(allx, ally, marker='o', color=gradient, edgecolor='royalblue', s=20)
    ax_path1.set_title('Путь курсора', fontsize=14)
    ax_path1.set_xlabel('X, px', c='dimgray', fontsize=12.5)
    ax_path1.set_ylabel('Y, px', c='dimgray', fontsize=12.5)
    ax_path1.invert_yaxis()
    ax_path1.set_aspect('equal')

    ax_path1.grid(which='major', color = 'dimgray')
    ax_path1.minorticks_on()
    ax_path1.grid(which='minor', color = 'gray', linestyle = ':')

    # Устанавливаем интервал основных и вспомогательных тиков
    ax_path1.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax_path1.xaxis.set_minor_locator(ticker.MultipleLocator(20))
    ax_path1.yaxis.set_major_locator(ticker.MultipleLocator(100))
    ax_path1.yaxis.set_minor_locator(ticker.MultipleLocator(20))

def create_graph_path2(ax_path2, allx, ally, gradient=None):
    # ax2.plot(allx, ally, "m--")
    ax_path2.plot(allx, ally, linestyle='-', linewidth = 1, marker='o', markersize=4, color='c')
    ax_path2.set_title('Путь курсора', fontsize=14)
    ax_path2.set_xlabel('координата X', c='dimgray', fontsize=12.5)
    ax_path2.set_ylabel('координата Y', c='dimgray', fontsize=12.5)
    ax_path2.invert_yaxis()
    ax_path2.set_aspect('equal')

    ax_path2.grid(which='major', color = 'dimgray')
    ax_path2.minorticks_on()
    ax_path2.grid(which='minor', color = 'gray', linestyle = ':')

    # Устанавливаем интервал основных и вспомогательных тиков
    ax_path2.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax_path2.xaxis.set_minor_locator(ticker.MultipleLocator(20))
    ax_path2.yaxis.set_major_locator(ticker.MultipleLocator(100))
    ax_path2.yaxis.set_minor_locator(ticker.MultipleLocator(20))

def create_graph_speed(ax_speed, time_, 
                       data_y, data_y_ex=None, data_y_smooth=None,
                       title='', ylabel='скорость px/ms',
                       gradient=None, c='m', linewidth=1.5):
    if data_y_smooth is not None:
        ax_speed.plot(time_, data_y, linewidth=1, linestyle='-', color='coral', label='по оси X')
        ax_speed.plot(time_, data_y_smooth, linewidth=linewidth, linestyle='-', color=c)
    else:
        ax_speed.plot(time_, data_y, linewidth=linewidth, linestyle='-', color=c, label='по оси X')
    if data_y_ex is not None:
        ax_speed.plot(time_, data_y_ex, linewidth=1, linestyle='-', color='darkgreen', label='по оси Y')
        ax_speed.legend()

    ax_speed.set_title(title, fontsize=14)
    ax_speed.set_xlabel('время, ms', c='dimgray', fontsize=12.5)
    ax_speed.set_ylabel(ylabel, c='dimgray', fontsize=12.5)

    ax_speed.grid(which='major', color = 'dimgray')
    ax_speed.yaxis.set_major_locator(ticker.MultipleLocator(1))
    maxabs = max(map(abs, data_y))
    if maxabs < 0.01:
        ax_speed.yaxis.set_major_locator(ticker.MultipleLocator(0.001))
    elif maxabs < 0.1:
        ax_speed.yaxis.set_major_locator(ticker.MultipleLocator(0.01))
    minor_grid_speed(ax_speed, data_y, maxabs)

def minor_grid_speed(_ax, data_y, maxabs):
    if maxabs <= 5.5:
        _ax.minorticks_on()
        _ax.grid(which='minor', color = 'gray', linestyle = ':')
    if 0.1 < maxabs <= 4:
        _ax.tick_params(axis = 'y', which = 'major', pad = 12)

    if maxabs < 0.01:
        _ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.0002))
    elif maxabs < 0.1:
        _ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.001))
        # _ax.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%.001f'))
    elif maxabs <= 4:
        _ax.tick_params(axis = 'both', which = 'minor', labelsize = 5, labelcolor = 'midnightblue')
        _ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
        _ax.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%.1f'))
    else:
        _ax.tick_params(axis = 'both', which = 'minor', labelsize = 6, labelcolor = 'midnightblue')
        _ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))


def cm_to_inch(value):
    return value/2.54


if __name__ == '__main__':
    _width = 100
    _hight = 50
    if sys.platform == 'win32':
        os.system('color 71')
        os.system('mode con cols=%d lines=%d' % (_width, _hight))
    cur_script = __file__
    PATH_SCRIPT = os.path.abspath(os.path.dirname(cur_script))
    os.chdir(PATH_SCRIPT)
    cc.clearConsol()

    __author__ = 'master by Vint'
    __title__ = '--- Graphic_report ---'
    __version__ = '0.2.0'
    __copyright__ = 'Copyright 2020 (c)  bitbucket.org/Vintets'
    auth_sh.authorship(__author__, __title__, __version__, __copyright__, width=_width)

    # filename = 'path_2020.11.16_14-29-20_points113.txt'
    filename = 'path_2020.11.16_13-49-40_points89.txt'

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            cp.cprint('2Передан параметр не соответствующий пути существующего файла')
            exit(1)
    elif not filename:
        cp.cprint('2Не задан файл с данными для построения')
        exit(1)

    try:
        mouse_graph_report(filename, imagesave=IMAGESAVE)
    except KeyboardInterrupt:
        print('Программа прервана пользователем')

    if not CLOSECONSOLE:
        input('\n---------------   END   ---------------')
    else:
        exit()

