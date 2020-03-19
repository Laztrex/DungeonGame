# -*- coding: utf-8 -*-
import decimal
import json
import re
from termcolor import cprint, colored
from dungeon_source.dungeon_walking import Dungeon
from dungeon_source.player_interface import DrownedManError, ExperienceError
from dungeon_source.represent_data import nested_list_analysis, user_input


class Game(Dungeon):
    """Ход игры"""
    def play_game(self):
        self.tree = self.open_map()
        while self.inspect_flag:
            self.player.stats_player(self)
            self.player.write_csv(self)
            cprint('\nПеред вами: ', color='blue')
            self.dungeon_descent(tree=self.tree)
            try:
                self._represent_users()
                self.check_flooding()
            except (ExperienceError, DrownedManError) as exc:
                cprint(exc, color='red')
                return self.player.name

    def open_map(self):
        with open(self.json_file, 'r') as file:
            loaded_json_file = json.load(file)
            return loaded_json_file

    def _represent_users(self):
        try:
            self.check_flooding()
            user_choice = user_input(self.actions)
            if not self.actions[user_choice][1](self.actions[user_choice][0]):
                nested_list_analysis(my_list=self.tree[self.current_stats['current_location']]).pop(user_choice)
                self.actions.pop(user_choice)
                self.next_location = False
            else:
                self.actions.clear()
            return True
        except (ValueError, IndexError):
            print(f'До следующей игры!')
            self.inspect_flag = 0

    def check_units(self, subject):
        if isinstance(subject, list):
            for elem in subject:
                print(self._define_action(unit=elem))
        else:
            print(self._define_action(unit=subject))

    def check_win(self, potential_hatch=None):
        if potential_hatch:
            hatch_time = decimal.Decimal(re.search(r'tm.*?(\d+(?:\.\d+)?)', potential_hatch).group(1))
            self.remaining_time -= hatch_time
            if self.current_stats['current_experience'] > 279 and self.check_flooding():
                self.inspect_flag = 0
                print('ВЫ НАШЛИ ВЫХОД!!!')
            else:
                raise ExperienceError
        else:
            return colored('Кажется, виднеется выход!', color='yellow')

    def check_flooding(self):
        if self.remaining_time <= 0:
            raise DrownedManError
        return True

    def _define_action(self, unit):
        if 'Mob' in unit:
            self._add_action(unit, self.kick_mobs)
            return f'- монстр <<{unit}>>'
        elif 'Location' in unit:
            self._add_action(unit, self.go_to_location)
            return f'- вход в локацию <<{unit}>>'
        elif 'Boss' in unit:
            self._add_action(unit, self.kick_boss)
            return f'- босс <<{unit}>>'
        else:
            if self.hatch.search(unit):
                self._add_action(unit, self.check_win)
                return f'- люк <<{unit}>>'
            else:
                return 'Неизвестные данные'

    def _add_action(self, obj, function):
        if self.next_location:
            self.actions.append((obj, function))

    def rebirth_at_beginning(self):
        cprint(self.player.reborn(), color='blue')
