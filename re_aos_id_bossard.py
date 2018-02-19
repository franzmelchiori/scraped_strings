#! /usr/bin/python


'''
Bossard AOS name and session ID provider
Wuerth Phoenix S.r.l., 2017

[<nome_aos>: Session ID - <session_number>]
<nome_aos>: BOSAXAP01, BOSAXAP02, BOSAXAP03, BOSAXBP1, BOSAXBP2, BOSAXFP1, BOSAXFP2, BOSAXAU1, BOSAXAU2
<session_number>: 0-65536
'''


import re


aos_names = ['AP01', 'AP02', 'AP03', 'BP1', 'BP2', 'FP1', 'FP2', 'AU1', 'AU2']
session_ids = range(65537)


def extract_aos_id(scrap_text):
    aos_pre = re.compile('Bossard AG \[').search(scrap_text)
    aos_post = re.compile(': Session ID').search(scrap_text)
    id_pre = re.compile('Session ID - ').search(scrap_text)
    id_post = re.compile('\] - \[[^a-zA-Z]').search(scrap_text)

    aos_name = scrap_text[aos_pre.end():aos_post.start()]
    session_id = scrap_text[id_pre.end():id_post.start()]
    return aos_name, session_id


if __name__ == "__main__":

    scrap_example = "Microsoft Dynamics AX - Bossard AG [BOSAXAP01: Session ID - 59] - [1 - dat] - [AX6_PROD@AXSQLPROD]"

    print 'aos_name =', extract_aos_id(scrap_example)[0]
    print 'session_id =', extract_aos_id(scrap_example)[1]
