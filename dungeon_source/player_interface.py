# -*- coding: utf-8 -*-
import datetime
import decimal
from csv import DictWriter
from termcolor import cprint


class DrownedManError(Exception):
    def __init__(self):
        self.name_error = 'YOU DIED'

    def __str__(self):
        return f'Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!! \n' \
               f'Время вышло. Подземелье затоплено! - {self.name_error} \n \n'


class ExperienceError(Exception):
    def __init__(self):
        self.name_error = "YOU ARE WEAK"

    def __str__(self):
        return f'\n \n У вас не хватило сил открыть люк! - {self.name_error} \n \n'


class Player:
    """Данные игрока"""

    def __init__(self, name):
        self.name = name if name else input('Введите ваше имя: ')
        self.xp = decimal.Decimal(0)

    def xp_up(self, val):
        self.xp += val

    def write_csv(self, game):
        with open("results_game.csv", "a") as csv_file:
            writer = DictWriter(csv_file, delimiter=',', lineterminator='\n', fieldnames=game.FIELD_NAMES)
            writer.writeheader() if not csv_file.tell() else writer.writerow(game.current_stats)

    def strfdelta(self, my_tdelta, str_format):
        """Строковое представление timedelta"""
        d = {}
        hours, rem = divmod(my_tdelta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        d["hours"] = '{:02d:}'.format(hours) if hours != 0 else ''
        d["minutes"] = '{:02d}'.format(minutes)
        d["seconds"] = '{:02d}'.format(seconds)
        return str_format.format(**d)

    def stats_player(self, game):
        """Вывод промежуточных итогов"""
        cprint(f'{chr(8595):^30}\n'
               f'Вы находитесь в {game.current_stats["current_location"]}\n'
               f'{chr(8593):^30}\n', color='cyan')
        cprint(f'{game.player} и {game.remaining_time} секунд до наводнения', color='grey')
        difference_seconds = datetime.datetime.now() - game.start_time
        cprint(f'Прошло времени: {self.strfdelta(difference_seconds, "{hours}{minutes}:{seconds}")}', color='grey')

    def reborn(self):
        return f'{self.name}, у вас темнеет в глазах... прощай, принцесса...\n' \
               f'Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)\n' \
               f'Ну, на этот-то раз у вас все получится! Трепещите, монстры!\n' \
               f'Вы осторожно входите в пещеру... \n \n '

    def __repr__(self):
        return f'{self.name} - {self.xp} опыта'
