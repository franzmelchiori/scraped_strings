#! /usr/bin/python


"""
    Fabbri 1905
    Processing of scraped strings
    AOS name and session ID provider
    Wuerth Phoenix S.r.l., 2017

    [<nome_aos>: Session ID - <session_number>]
    <nome_aos>: FABAX6PAOS1, FABAX6PAOS2, FABAX6PAOS3
    <session_number>: 0-65536
"""


import scraped_strings
import sqlite3


def check_fabbri_aos_name(raw_aos_name=''):
    fabbri_aos_names = ['FABAX6PAOS1', 'FABAX6PAOS2', 'FABAX6PAOS3']
    if raw_aos_name:
        if raw_aos_name in fabbri_aos_names or raw_aos_name is 'unreadable':
            return raw_aos_name
        else:
            return 'unknown'
    return 'empty'


def extract_fabbri_aos_id_str(scrap_text='', mark_start='', mark_middle='', mark_stop='', mark_aos='aos'):
    aos_name, session_id = scraped_strings.extract_aos_id_str(scrap_text=scrap_text,
                                                              mark_start=mark_start,
                                                              mark_middle=mark_middle,
                                                              mark_stop=mark_stop,
                                                              mark_aos=mark_aos)
    aos_name = check_fabbri_aos_name(aos_name)
    return aos_name, session_id


if __name__ == "__main__":

    print('alyvix fabbri1905 scrap solver')
    while True:
        command = raw_input('enter command: ')

        if command == 'solve_scraps':
            fabbri_db_path = r'C:\projects\python_scraped_strings\fabbri1905_ax12r3_sales.sqlite'
            query_template = 'SELECT scraped_text FROM ax_aos_id ORDER BY transaction_timestamp DESC LIMIT ?;'
            limit = 100
            query_requests = (limit, )

            fabbri_db_connection = sqlite3.connect(fabbri_db_path)
            fabbri_db_cursor = fabbri_db_connection.cursor()

            for fabbri_scraped_ax_aos_id in fabbri_db_cursor.execute(query_template, query_requests):
                print(fabbri_scraped_ax_aos_id)
                print(extract_fabbri_aos_id_str(fabbri_scraped_ax_aos_id[0],
                                                'S.p.A. [',
                                                ': ID sessione - ',
                                                '] - ['))

            fabbri_db_connection.close()

        if command == 'solve_scrap':
            scrap_example =             "Microsoft Dynamics AX - Fabbri G. Holding Industriale S.p.A. [FABAX6PAOS2: ID sessione - 1] - [1 - fa10]"
            rotten_scrap_example =      "Microsoft Dynamics AX - Fabbri G. Holding Industriale S.p.A. [FABAX6PAOSZ: ID sessione - 1] - [1 - fa10]"
            superrotten_scrap_example = "Microsoft Dynamics AX - Fabbri 6. Holding Industriale S.p.A. [FABla6PAOSZ: ID sessione - 11 - [1 - fa10]"

            print(extract_fabbri_aos_id_str(rotten_scrap_example,
                                            'S.p.A. [',
                                            ': ID sessione - ',
                                            '] - ['))

            print(extract_fabbri_aos_id_str(superrotten_scrap_example,
                                            'S.p.A. [',
                                            ': ID sessione - ',
                                            '] - ['))

        if command == 'exit':
            break

    print('end.')
