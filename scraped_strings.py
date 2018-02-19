#! /usr/bin/python

"""
    Text processing of OCR scraped strings
    Copyright (C) 2018 Francesco Melchiori <https://www.francescomelchiori.com/>

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

import re


class StringManager:

    def __init__(self, bla):
        self.bla = bla


def store_json_ip_hostname_map(self):
    ip_hostname_map = {'192.168.0.1': 'hostname_1',
                       '192.168.0.2': 'hostname_2'}
    json.dump(ip_hostname_map,
              fp=open('{0}_ip_hostname_map.json'.format(self.customer_name), 'w'),
              indent=4)

def load_json_ip_hostname_map(self, path_json=''):
    filename_json = '{0}_ip_hostname_map.json'.format(self.customer_name)
    path_json_ip_hostname_map = '{0}{1}'.format(path_json, filename_json)
    try:
        self.ip_hostname_map = json.load(open(path_json_ip_hostname_map))
    except IOError:
        print('{0}_ip_hostname_map.json does not exist'.format(self.customer_name))
        return False
    return True

def scraping_cleaner(scraped_string='', mark=''):
    cleaned_string = ''
    if scraped_string != '':
        scraped_string = scraped_string.lower()
        if mark != '':
            where_mark = scraped_string.find(mark)
            if where_mark != -1:
                mark_length = mark.__len__()
                strip_string = scraped_string[(where_mark + mark_length):]
            else:
                return cleaned_string
        else:
            strip_string = scraped_string.strip()
        cleaned_string = ''.join(strip_string.split())
    return cleaned_string

def extract_aos_id_str(scrap_text='', mark_start='', mark_middle='', mark_stop='', mark_aos = 'aos'):
    aos_name, session_id = '', ''
    if scrap_text != '':
        mark_start = mark_start
        where_mark = scrap_text.find(mark_start)
        if where_mark != -1:
            mark_length = mark_start.__len__()
            scrap_text = scrap_text[(where_mark + mark_length):]

            mark_middle = mark_middle
            where_mark = scrap_text.find(mark_middle)
            if where_mark != -1:
                mark_length = mark_middle.__len__()
                aos_name = scrap_text[:where_mark]
                scrap_text = scrap_text[(where_mark + mark_length):]

                mark_aos = mark_aos.lower()
                where_aos = aos_name.lower().find(mark_aos)
                if where_aos != -1:
                    mark_length = mark_aos.__len__()
                    aos_name_prefix = aos_name[:(where_aos + mark_length)].strip()
                    aos_number_raw = aos_name[(where_aos + mark_length):].strip()
                    aos_number_fix = aos_number_raw.lower().replace('z', '2')
                    aos_name = ''.join([aos_name_prefix, aos_number_fix])

                mark_stop = mark_stop
                where_mark = scrap_text.find(mark_stop)
                if where_mark != -1:
                    session_id = scrap_text[:where_mark].strip()

    if not aos_name:
        aos_name = 'unreadable'
    if not session_id.isdigit():
        session_id = '-1'
    return str(aos_name), str(session_id)

def extract_aos_id_re(scrap_text, mark_1='', mark_2='', mark_3='', mark_4=''):
    aos_pre = re.compile(mark_1).search(scrap_text)
    aos_post = re.compile(mark_2).search(scrap_text)
    id_pre = re.compile(mark_3).search(scrap_text)
    id_post = re.compile(mark_4).search(scrap_text)

    aos_name = scrap_text[aos_pre.end():aos_post.start()]
    session_id = scrap_text[id_pre.end():id_post.start()]
    return aos_name, session_id

def check_customer_name_aos_name(raw_aos_name=''):
    customer_name_aos_names = ['CUNAX6PAOS1', 'CUNAX6PAOS2', 'CUNAX6PAOS3']
    if raw_aos_name:
        if raw_aos_name in customer_name_aos_names or raw_aos_name is 'unreadable':
            return raw_aos_name
        else:
            return 'unknown'
    return 'empty'

def extract_customer_name_aos_id_str(scrap_text='', mark_start='', mark_middle='', mark_stop='', mark_aos='aos'):
    aos_name, session_id = extract_aos_id_str(scrap_text=scrap_text,
                                              mark_start=mark_start,
                                              mark_middle=mark_middle,
                                              mark_stop=mark_stop,
                                              mark_aos=mark_aos)
    aos_name = check_customer_name_aos_name(aos_name)
    return aos_name, session_id


if __name__ == "__main__":

    scrap_example_01 = "S.p.A. [AOS2: ID sessione - 1] - [1 -"
    scrap_example_02 = "GmbH & Co KG [1869ASOO11: Session ID - 39] - [1 -"
    rotten_scrap_example_01 = "S.p.A. [AOSZ: ID sessione - 1] - [1 -"
    rotten_scrap_example_02 = "S.p.A. [AOSZ: ID sessione - 11 - [1 -"

    print(extract_aos_id_str(scrap_example_01, 'S.p.A. [', ': ID sessione - ', '] - ['))
    print(extract_aos_id_str(scrap_example_02, 'GmbH & Co KG [', ': Session ID - ', '] - ['))
    print(extract_customer_name_aos_id_str(rotten_scrap_example_01, 'S.p.A. [', ': ID sessione - ', '] - ['))
    print(extract_customer_name_aos_id_str(rotten_scrap_example_02, 'S.p.A. [', ': ID sessione - ', '] - ['))
