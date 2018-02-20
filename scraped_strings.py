#! /usr/bin/python

"""
    Text processing of OCR scraped strings
    Copyright (C) 2018 Francesco Melchiori
    <https://www.francescomelchiori.com/>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json


class StringManager:

    def __init__(self, scraped_string, customer_name='test', path_json='',
                 map_norm=True):
        self.scraped_string = str(scraped_string)
        self.aos_scrap = 'no_aos_scrap'
        self.id_scrap = 'no_id_scrap'
        self.aos_name = 'no_aos_name'
        self.id_session = 'no_id_session'
        self.customer_name = str(customer_name)
        self.path_json = str(path_json)
        self.customer_settings = {}
        if customer_name == 'test':
            self.store_json_customer_settings()
        self.load_json_customer_settings(self.path_json)
        self.map_norm = map_norm
        self.extract_aos_name()
        self.extract_id_session()

    def print_aos_name(self):
        if self.aos_scrap != '':
            print(self.aos_scrap)
        else:
            print('no aos name')
        return True

    def print_id_session(self):
        if self.id_scrap != '':
            print(self.id_scrap)
        else:
            print('no id session')
        return True

    def store_json_customer_settings(self):
        customer_settings = {'aos_names': ['aos_1', 'aos_2'],
                             'ax_title_marks': {'aos_start': 'Inc. [',
                                                'aos_stop': ': Session',
                                                'id_start': 'ID - ',
                                                'id_stop': '] - ['}}
        json.dump(customer_settings,
                  fp=open('{0}_customer_settings.json'.format(
                      self.customer_name), 'w'),
                  indent=4)
        return True

    def load_json_customer_settings(self, path_json=''):
        filename_json = '{0}_customer_settings.json'.format(self.customer_name)
        path_json_customer_settings = '{0}{1}'.format(path_json, filename_json)
        try:
            self.customer_settings = json.load(open(
                path_json_customer_settings))
        except IOError:
            print('{0}_customer_settings.json does not exist'.format(
                self.customer_name))
            return False
        return True

    def extract_text_scrap(self, mark_start='', mark_stop=''):
        if self.scraped_string != '':
            cut_start = self.scraped_string.find(mark_start)
            cut_stop = self.scraped_string.find(mark_stop)
            if cut_start != -1 and cut_stop != -1:
                cut_start += mark_start.__len__()
                text_scrap = self.scraped_string[cut_start:cut_stop].strip()
                return text_scrap
        return False

    def extract_aos_name(self):
        if 'ax_title_marks' in self.customer_settings:
            ax_title_marks = self.customer_settings['ax_title_marks']
            aos_start = ax_title_marks['aos_start']
            aos_stop = ax_title_marks['aos_stop']
            text_scrap = self.extract_text_scrap(mark_start=aos_start,
                                                 mark_stop=aos_stop)
            if text_scrap:
                self.aos_scrap = text_scrap
                if self.map_norm:
                    self.map_aos_scrap()
                return True
        return False

    def extract_id_session(self):
        if 'ax_title_marks' in self.customer_settings:
            ax_title_marks = self.customer_settings['ax_title_marks']
            id_start = ax_title_marks['id_start']
            id_stop = ax_title_marks['id_stop']
            text_scrap = self.extract_text_scrap(mark_start=id_start,
                                                 mark_stop=id_stop)
            if text_scrap:
                self.id_scrap = text_scrap
                if self.map_norm:
                    self.norm_id_session()
                return True
        return False

    def map_aos_scrap(self):
        if 'aos_names' in self.customer_settings:
            aos_names = self.customer_settings['aos_names']
            if self.aos_scrap in aos_names:
                self.aos_name = self.aos_scrap
                return True
            else:
                pass
        return False

    def norm_id_session(self):
        try:
            norm_id_scrap = int(''.join(self.id_scrap.split()))
        except ValueError:
            return False
        if norm_id_scrap in range(2**16):
            self.id_session = norm_id_scrap
            return True
        return False


def get_aos_id(scraped_string, customer_name='test', path_json='',
               map_norm=True):
    sm = StringManager(scraped_string=scraped_string,
                       customer_name=customer_name,
                       path_json=path_json,
                       map_norm=map_norm)
    if map_norm:
        return sm.aos_name, sm.id_session
    return sm.aos_scrap, sm.id_scrap


if __name__ == "__main__":

    scrap_example_us = "Inc. [a0s_1: Session ID - 1 2] - [1 -"
    scrap_example_it = "S.p.A. [a0s_1: ID sessione - 1 2] - [1 -"
    scrap_example_de = "GmbH [a0s_1: Session ID - 1 2] - [1 -"

    print(get_aos_id(scraped_string=scrap_example_us,
                     customer_name='test',
                     map_norm=True))
