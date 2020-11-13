#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import accessory.colorprint as cp
import accessory.clear_consol as cc
import accessory.authorship as auth_sh
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import cm


CLOSECONSOLE = True

# ==================================================================================================

def mouse_graph_report(filename):
    points = filedata_read(filename)
    # print(points)

    allx = [point[0] for point in points]
    ally = [point[1] for point in points]
    time_ = [point[2] for point in points]

    speedx = calculate_speed_axis(points, axis=0)
    speedy = calculate_speed_axis(points, axis=1)
    speed = calculate_speed(points)

    gradient = create_gradient(len(points))
    create_graphs(allx=allx, ally=ally, speedx=speedx, speedy=speedy, speed=speed, time_=time_, gradient=gradient)

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

def create_graphs(
                allx, ally,
                speedx, speedy,
                speed,
                time_,
                gradient):
    fig, ((ax1, ax3, ax5), (ax2, ax4, ax6)) = plt.subplots(
                                nrows=2,
                                ncols=3,
                                figsize=(cm_to_inch(35), cm_to_inch(20)),
                                dpi=100,
                                facecolor='#EEEEEE'
                                )
    fig.canvas.set_window_title('Сумашедшая мышь')
    fig.set_tight_layout(True)

    create_graph_path1(ax1, gradient, allx, ally)
    create_graph_path2(ax2, gradient, allx, ally)
    create_graph_speedx(ax3, gradient, time_, speedx)
    create_graph_speedy(ax4, gradient, time_, speedy)
    create_graph_speed(ax5, gradient, time_, speed)

    plt.tight_layout()
    plt.show()
    plt.close()

def create_graph_path1(ax1, gradient, allx, ally):
    ax1.scatter(allx, ally, marker='o', color=gradient, edgecolor='royalblue', s=20)
    ax1.set_title('Путь курсора')
    ax1.set_xlabel('X, px', c='g', fontsize=14)
    ax1.set_ylabel('Y, px', c='g', fontsize=14)
    ax1.invert_yaxis()
    ax1.set_aspect('equal')

    ax1.grid(which='major', color = 'dimgray')
    ax1.minorticks_on()
    ax1.grid(which='minor', color = 'gray', linestyle = ':')

    # Устанавливаем интервал основных и вспомогательных тиков
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax1.xaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(100))
    ax1.yaxis.set_minor_locator(ticker.MultipleLocator(10))

def create_graph_path2(ax2, gradient, allx, ally):
    # ax2.plot(allx, ally, "m--")
    ax2.plot(allx, ally, linestyle='-', linewidth = 1, marker='o', markersize=4, color='c')
    ax2.set_title('Путь курсора')
    ax2.set_xlabel('координата X', c='g', fontsize=14)
    ax2.set_ylabel('координата Y', c='g', fontsize=14)
    ax2.invert_yaxis()
    ax2.set_aspect('equal')

    ax2.grid(which='major', color = 'dimgray')
    ax2.minorticks_on()
    ax2.grid(which='minor', color = 'gray', linestyle = ':')

    # Устанавливаем интервал основных и вспомогательных тиков
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(100))
    ax2.yaxis.set_minor_locator(ticker.MultipleLocator(10))

def create_graph_speedx(ax3, gradient, time_, speedx):
    ax3.plot(time_, speedx, linestyle='-', color='m')
    ax3.set_title('Скорость по X')
    ax3.set_xlabel('время, ms', c='dimgray', fontsize=14)
    ax3.set_ylabel('скорость px/ms', c='dimgray', fontsize=14)
    # ax3.invert_yaxis()
    # ax3.set_aspect('equal')

    ax3.grid(which='major', color = 'dimgray')
    ax3.minorticks_on()
    ax3.grid(which='minor', color = 'gray', linestyle = ':')

    # Устанавливаем интервал основных и вспомогательных тиков
    # ax3.xaxis.set_major_locator(ticker.MultipleLocator(100))
    # ax3.xaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax3.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax3.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    ax3.tick_params(axis = 'both',
                    which = 'minor',
                    labelsize = 6
                    )
    ax3.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%.1f'))

def create_graph_speedy(ax4, gradient, time_, speedy):
    ax4.plot(time_, speedy, linestyle='-', color='m')
    ax4.set_title('Скорость по Y')
    ax4.set_xlabel('время, ms', c='dimgray', fontsize=14)
    ax4.set_ylabel('скорость px/ms', c='dimgray', fontsize=14)
    # ax4.invert_yaxis()
    # ax4.set_aspect('equal')

    ax4.grid(which='major', color = 'dimgray')
    ax4.minorticks_on()
    ax4.grid(which='minor', color = 'gray', linestyle = ':')

    # Устанавливаем интервал основных и вспомогательных тиков
    # ax4.xaxis.set_major_locator(ticker.MultipleLocator(100))
    # ax4.xaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax4.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax4.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    ax4.tick_params(axis = 'both',
                    which = 'minor',
                    labelsize = 6
                    )
    ax4.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%.1f'))

def create_graph_speed(ax5, gradient, time_, speed):
    ax5.plot(time_, speed, linestyle='-', color='m')
    ax5.set_title('Скорость курсора')
    ax5.set_xlabel('время, ms', c='dimgray', fontsize=14)
    ax5.set_ylabel('скорость px/ms', c='dimgray', fontsize=14)
    # ax5.invert_yaxis()
    # ax5.set_aspect('equal')

    ax5.grid(which='major', color = 'dimgray')
    ax5.minorticks_on()
    ax5.grid(which='minor', color = 'gray', linestyle = ':')

    # Устанавливаем интервал основных и вспомогательных тиков
    # ax5.xaxis.set_major_locator(ticker.MultipleLocator(100))
    # ax5.xaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax5.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax5.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    ax5.tick_params(axis = 'both',
                    which = 'minor',
                    labelsize = 6
                    )
    ax5.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%.1f'))

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
    __version__ = '0.1.0'
    __copyright__ = 'Copyright 2020 (c)  bitbucket.org/Vintets'
    auth_sh.authorship(__author__, __title__, __version__, __copyright__, width=_width)

    # filename = 'path_2020.11.11_13-46-25_points42.txt'
    # filename = 'path_2020.11.13_14-56-42_points79.txt'
    filename = 'path_2020.11.13_19-25-45_points48.txt'

    if(len(sys.argv) > 1):
        filename = sys.argv[1]

    try:
        mouse_graph_report(filename)
    except KeyboardInterrupt:
        print('Программа прервана пользователем')

    if not CLOSECONSOLE:
        input('\n---------------   END   ---------------')
    else:
        exit()

