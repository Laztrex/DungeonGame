# -*- coding: utf-8 -*-
import time
from termcolor import cprint


def user_input(data, choice=None):
    cprint('\n Выберете действие: ', color='yellow')
    for num, bound_actions in enumerate(data):
        print(f'{num + 1}. {bound_actions[1]()}')
    print(f'{len(data) + 1}. Сдаться и выйти из игры')
    while True:
        try:
            choice = int(input("Ваш ход: ")) - 1
            assert choice > - 1
            cprint(f'\n \n Вы выбрали {data[choice][1]()} <<{data[choice][0]}>> \n \n', color='magenta')
        except (IndexError, AssertionError):
            if choice == len(data):
                raise
            else:
                print('Такого варианта нет. Попробуйте еще раз')
                continue
        except ValueError:
            print('Это не целочисленное значение. Попробуйте еще раз')
            continue
        else:
            break
    time.sleep(0.8)
    return choice


def nested_list_analysis(my_list):
    """Проверка на вложенные списки"""
    if isinstance(my_list[0], list):
        return my_list[0]
    else:
        return my_list
