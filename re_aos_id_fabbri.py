#! /usr/bin/python


'''
Fabbri 1905 AOS name and session ID provider
Wuerth Phoenix S.r.l., 2017

[<nome_aos>: Session ID - <session_number>]
<nome_aos>: BOSAXAP01, BOSAXAP02, BOSAXAP03, BOSAXBP1, BOSAXBP2, BOSAXFP1, BOSAXFP2, BOSAXAU1, BOSAXAU2
<session_number>: 0-65536
'''


import re


aos_names = ['FABAX6PAOS1', 'FABAX6PAOS2', 'FABAX6PAOS3']
session_ids = range(65537)
sql_path = r'C:\projects\python_re\fabbri1905_ax12r3_sales.sqlite'


def extract_aos_id(scrap_text):
    aos_pre = re.compile('Industriale S.p.A. \[').search(scrap_text)
    aos_post = re.compile(': ID sessione').search(scrap_text)
    id_pre = re.compile('ID sessione - ').search(scrap_text)
    id_post = re.compile('\] - \[[^a-zA-Z]').search(scrap_text)

    aos_name = scrap_text[aos_pre.end():aos_post.start()]
    session_id = scrap_text[id_pre.end():id_post.start()]
    return aos_name, session_id


if __name__ == "__main__":

    scrap_example = "Microsoft Dynamics AX - Fabbri G. Holding Industriale S.p.A. [FABAX6PAOSZ: ID sessione - 227] - [1 - fa10]"

    print 'aos_name =', extract_aos_id(scrap_example)[0]
    print 'session_id =', extract_aos_id(scrap_example)[1]
