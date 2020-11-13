#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import accessory.colorprint as cp
import accessory.clear_consol as cc
import accessory.authorship as auth_sh
import pyautogui
import keyboard


CLOSECONSOLE = True
RECORD = False
EXIT_SCRIPT = False


# ==================================================================================================

def main(count):
    cp.cprint('1Управление:')
    cp.cprint('2_1 - ^1_Запустить запись координат')
    cp.cprint('4_2 - ^1_Остановить запись координат')
    cp.cprint('9Ctrl+Q - ^1_Выход')
    print('♦'*100, '')

    add_hotkeys()

    num_path = 0
    data = []
    while(True):
        if EXIT_SCRIPT:
            exit_action(data)
        if(RECORD):
            num_path = record_path(data, num_path=num_path)
        time.sleep(0.1)

def add_hotkeys():
    keyboard.add_hotkey('1', hotkey_start)
    keyboard.add_hotkey('2', hotkey_stop)
    keyboard.add_hotkey('Ctrl+Q', hotkey_exit)

def hotkey_start():
    global RECORD
    if RECORD: return
    RECORD = True
    cp.cprint2('2Запись...')

def hotkey_stop():
    global RECORD
    if not RECORD: return
    RECORD = False
    cp.cprint2('4Stop')

def hotkey_exit():
    global EXIT_SCRIPT
    EXIT_SCRIPT = True
    global RECORD
    RECORD = False
    # keyboard.unhook_all_hotkeys()
    cp.cprint('0\n\nЗаписываем файл...')

def exit_action(data):
    for i, path in enumerate(data):
        # savefile(path)
        print('path № ', i)
        for item in path:
            print(item)
        print()
    sys.exit()

def record_path(data, num_path=0):
    coords_path = []
    time_start = time.time()
    while(RECORD):
        xmouse, ymouse = pyautogui.position()
        position = (xmouse, ymouse, (time.time() - time_start) * 1000)
        coords_path.append(position)
        cp.cprint2('2\rЗапись №{num: >2} ^14_x{x: >4} ^15_y{y: >4}  ^8_time{time: <18}  '.format(
                                                        x=position[0],
                                                        y=position[1],
                                                        time=position[2],
                                                        num=num_path
                                                        ))
        time.sleep(0.001)  # сколько ни ставь, минимум 15~16 ms
    else:
        cp.cprint( '2\rЗапись №{num: >2} ^14_x{x: >4} ^15_y{y: >4}  ^8_time{time: <18}  ^4_Stop  ^0_► len {length} points'.format(
                                                        x=position[0],
                                                        y=position[1],
                                                        time=position[2],
                                                        num=num_path,
                                                        length=len(coords_path)
                                                        ))
        data.append(coords_path)
        savefile(coords_path)
        num_path += 1
    return num_path

def savefile(path):
    current_time = time.strftime('%Y.%m.%d_%H-%M-%S', time.localtime(time.time()))
    filename = f'path_{current_time}_points{len(path)}.txt'
    text_path = [' '.join(map(str, item)) for item in path]
    with open(filename, 'w', encoding='utf-8') as fw:
        fw.write('\n'.join(text_path))
    time.sleep(1)


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
    __title__ = '--- Mouse_record ---'
    __version__ = '0.0.1'
    __copyright__ = 'Copyright 2020 (c)  bitbucket.org/Vintets'
    auth_sh.authorship(__author__, __title__, __version__, __copyright__, width=_width)

    count = 1

    try:
        main(count)
    except KeyboardInterrupt:
        print('Программа прервана пользователем')

    if not CLOSECONSOLE:
        input('\n---------------   END   ---------------')
    else:
        # time.sleep(1)
        exit()
