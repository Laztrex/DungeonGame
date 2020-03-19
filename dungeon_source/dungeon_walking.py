# -*- coding: utf-8 -*-
import datetime
import decimal
import re
from abc import ABCMeta, abstractmethod
from collections import defaultdict, Counter
from termcolor import colored
from dungeon_source.player_interface import Player


class Dungeon(metaclass=ABCMeta):
    """Манипуляции с подземельем"""
    FIELD_NAMES = ['current_location', 'current_experience', 'current_date']

    def __init__(self, file, player=None):
        self.remaining_time = decimal.Decimal('123456.0987654321')
        self.inspect_flag = 1
        self.current_stats = Counter(dict.fromkeys(self.FIELD_NAMES, 0))
        self.current_stats['current_location'] = 'Location_0_tm0'
        self.current_stats['current_date'] = datetime.datetime.now().strftime("%d.%m.%Y, %H.%M.%S")
        self.hatch = re.compile(r'[Hh]atch')

        self.player = Player(name=player)
        self.json_file = file
        self.actions = []
        self.start_time = datetime.datetime.now()
        self.tree = defaultdict()
        self.next_location = True

    @abstractmethod
    def check_units(self, subject):
        pass

    def dungeon_descent(self, tree):
        """Проход по дереву tree"""
        if isinstance(tree, dict):
            return self.dungeon_descent(tree[self.current_stats['current_location']])
        for sub in tree:
            if isinstance(sub, dict):
                self.tree.update(sub)
                for location, list_actions in sub.items():
                    self.check_units(location)
            else:
                self.check_units(sub)

    def kick_mobs(self, sub=None):
        if sub:
            xp_up = decimal.Decimal(re.search(r'exp.*?(\d+)', sub).group(1))
            self.player.xp_up(val=xp_up)
            self.current_stats['current_experience'] = self.player.xp
            battle_time = decimal.Decimal(re.search(r'tm.*?(\d+(?:\.\d+)?)', sub).group(1))
            self.remaining_time -= battle_time
            return False
        else:
            return colored("Атаковать монстра", 'red')

    def kick_boss(self, sub=None):
        if sub:
            return self.kick_mobs(sub)
        else:
            return colored("Атаковать босса", 'red')

    def go_to_location(self, current=None):
        if current:
            transition_time = decimal.Decimal(re.search(r'tm.*?(\d+(?:\.\d+)?)', current).group(1))
            self.remaining_time -= transition_time
            self.current_stats['current_location'] = current
            self.tree = {current: self.tree[current]}
            self.next_location = True
            return True
        else:
            return colored("Перейти в локацию", 'cyan')
