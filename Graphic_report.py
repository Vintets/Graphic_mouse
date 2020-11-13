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

CLOSECONSOLE = True

# ==================================================================================================

def mouse_graph_report(filename):
    points = filedata_read(filename)
    # print(points)

    allx = [point[0] for point in points]
    ally = [point[1] for point in points]
    create_graph(points, allx=allx, ally=ally)
    return

    plt.close()
    # Маркер начала окружности
    plt.plot(tx,ty,linestyle='',marker=',',markersize=10, markerfacecolor='#0000FF')
    plt.plot(mx1,my1,linestyle='',marker='.',markersize=10, markerfacecolor='#0000FF')


    def is_file_exists(self, file):
        return os.path.exists(file)


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

def create_graph(points, allx=None, ally=None):
    fig, (ax1, ax2) = plt.subplots(
                                nrows=1,
                                ncols=2,
                                figsize=(cm_to_inch(25), cm_to_inch(10)),
                                dpi=100,
                                facecolor='#EEEEEE'
                                )
    fig.canvas.set_window_title('Сумашедшая мышь')
    fig.set_tight_layout(True)

    ax1.scatter(allx, ally, marker='o', c='c', edgecolor='b')
    ax1.set_title('Путь курсора')
    ax1.set_xlabel('X, px', c='g', fontsize=14)
    ax1.set_ylabel('Y, px', c='g', fontsize=14)
    ax1.invert_yaxis()

    ax1.grid(which='major', color = 'k')
    ax1.minorticks_on()
    ax1.grid(which='minor', color = 'gray', linestyle = ':')

    # ax2.plot(allx, ally, "m--")
    ax2.plot(allx, ally, linestyle='--', marker='o', color='c')
    ax2.set_title('Путь курсора')
    ax2.set_xlabel('координата X', c='g', fontsize=14)
    ax2.set_ylabel('координата Y', c='g', fontsize=14)
    ax2.invert_yaxis()

    ax2.grid(which='major', color = 'k')
    ax2.minorticks_on()
    ax2.grid(which='minor', color = 'gray', linestyle = ':')

    plt.tight_layout()
    plt.show()

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

    filename = 'path_2020.11.11_13-46-25.txt'
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
