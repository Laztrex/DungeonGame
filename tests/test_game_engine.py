# -*- coding: utf-8 -*-
import decimal
import os
import unittest
from termcolor import cprint
from unittest.mock import patch, call
from dungeon_source.game_engine import Game


class GlobalEngineTest(unittest.TestCase):
    VALUE_MAIN_TEST = ['1'] * 15
    FIELDS_MAIN_TEST = {'current_experience': decimal.Decimal('279'),
                        'time_out': decimal.Decimal('592.0000000001')}

    VALUE_INCORRECT_TEST = ['!', '111', '22', 'ПАМАГИТЕ', '5', '!', 'energy', 'Doom:Eternal', '@', '4']
    VALUE_CHECK_UNITS_TEST = [('Location_1_tm1040', "- вход в локацию <<Location_1_tm1040>>"),
                              ("Mob_exp20_tm200", "- монстр <<Mob_exp20_tm200>>"),
                              ("Location_9_tm26000", "- вход в локацию <<Location_9_tm26000>>"),
                              ("Mob_exp40_tm50", "- монстр <<Mob_exp40_tm50>>"),
                              ("Hatch_tm159.098765432", "- люк <<Hatch_tm159.098765432>>"),
                              ("Boss_exp280_tm10400000", "- босс <<Boss_exp280_tm10400000>>")]

    VALUE_ALMOST_OPENED = ['3', '1', '2', '2', '1', '1', '1', '1', '1', '1', '1', '1']

    def setUp(self):
        self.game_test = \
            Game(file=os.path.join(os.path.dirname(os.getcwd()), 'rpg_map.json'), player='Петя')
        cprint(f'Вызван {self.shortDescription()}', flush=True, color='cyan')
        self.time_control = decimal.Decimal('123456.0987654321')

    def tearDown(self):
        cprint(f'Оттестировано. \n', flush=True, color='grey')

    @patch('time.sleep', return_value=None)
    @patch('builtins.print', return_value=None)
    def test_main_game(self, mocked_time, mocked_print):
        """Тест при корректной работе"""
        with patch('builtins.input', side_effect=self.VALUE_MAIN_TEST):
            self.game_test.play_game()
        self.assertEqual(self.game_test.current_stats['current_experience'],
                         self.FIELDS_MAIN_TEST['current_experience'])
        self.assertEqual(self.game_test.remaining_time, self.FIELDS_MAIN_TEST['time_out'])

    @patch('builtins.print', return_value=None)
    @patch('time.sleep', return_value=None)
    @patch('builtins.input', side_effect=VALUE_INCORRECT_TEST)
    def test_incorrect_input(self, mocked_input, mocked_time, mocked_print):
        """Тест с неправильным вводом"""
        # Подразумевается, что если не "4", то _infinite_loop_ в user_input()
        self.game_test.play_game()
        self.assertEqual(self.game_test.inspect_flag, 0)

    @patch('time.sleep', return_value=None)
    @patch('builtins.print')
    def test_check_units(self, mock_print, mocked_time):
        """Тест на правильность распознавания действий"""
        for unit, repr_unit in self.VALUE_CHECK_UNITS_TEST:
            self.game_test.check_units(unit)
            mock_print.assert_has_calls([call(repr_unit)])

    @patch('builtins.print', return_value=None)
    @patch('time.sleep', return_value=None)
    def test_not_winner(self, mocked_time, mocked_print):
        """Тест возможности открытия люка - 1"""
        # В модуле game_engine.py при не выполнении условия срабатывает exception ExperienceError
        # Метод play_game() возвращает в основной модуль имя игрока, цикл начинается заново
        with patch('builtins.input', side_effect=self.VALUE_ALMOST_OPENED):
            self.assertEqual(self.game_test.play_game(), 'Петя')

    @patch('builtins.print', return_value=None)
    @patch('time.sleep', return_value=None)
    def test_drowned(self, mocked_time, mocked_print):
        """Тест возможности открытия люка - 2"""
        # Принцип проверки схож с test_not_winner
        a = self.VALUE_ALMOST_OPENED.copy()
        a.insert(0, '1')
        a[1] = '2'
        self.game_test.remaining_time = decimal.Decimal('123456.0987654320')
        with patch('builtins.input', side_effect=a):
            self.assertEqual(self.game_test.play_game(), 'Петя')

    @patch('builtins.print', return_value=None)
    @patch('time.sleep', return_value=None)
    def test_winner(self, mocked_time, mocked_print):
        """Тест возможности открытия люка - 3"""
        # Цикл в 01_dungeon прерывается при открытии люка
        a = self.VALUE_ALMOST_OPENED.copy()
        a.insert(0, '1')
        a[1] = '2'
        with patch('builtins.input', side_effect=a):
            self.game_test.play_game()
            self.assertEqual(self.game_test.inspect_flag, 0)

    @patch('builtins.print', return_value=None)
    @patch('time.sleep', return_value=None)
    def test_reg_exp(self, mocked_time, mocked_print):
        """Тест регулярных выражений в лоб"""
        test_battle = Game(file="rpg.json", player='Алёша')
        test_battle.kick_mobs('Mob_exp40_tm50')
        self.assertEqual(test_battle.current_stats['current_experience'], decimal.Decimal('40'))
        self.assertNotEqual(test_battle.remaining_time, self.time_control - decimal.Decimal('49.99999'))
        self.assertEqual(test_battle.remaining_time, self.time_control - decimal.Decimal('50'))

        test_boss = Game(file="rpg.json", player='Тёма')
        test_boss.kick_boss('Boss200_exp30_tm10')
        self.assertEqual(test_boss.current_stats['current_experience'], decimal.Decimal('30'))
        self.assertNotEqual(test_boss.remaining_time, self.time_control - decimal.Decimal('9.99999'))
        self.assertEqual(test_boss.remaining_time, self.time_control - decimal.Decimal('10'))

        test_location = Game(file="rpg.json", player='Спелеолог')
        test_location.tree = {'Location_12_tm0.0987654320': ['Boss100_exp100_tm10', 'Boss200_exp30_tm10']}
        test_location.go_to_location('Location_12_tm0.0987654320')
        self.assertNotEqual(test_location.remaining_time, self.time_control - decimal.Decimal('0.0987654321'))
        self.assertEqual(test_location.remaining_time, self.time_control - decimal.Decimal('0.0987654320'))


if __name__ == '__main__':
    unittest.main()
