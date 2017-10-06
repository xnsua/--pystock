# import re
# import urllib
# from typing import List
#
# import pyquery
# from ghost import Ghost
#
# from common import key_value_db
# from common.web_helper import firefox_download_file, firefox_quick_download_file
# from project_config.config_module import myconfig, ppath
#
# ghost = Ghost()
# _db = key_value_db.KeyValueDb()
#
# class Disclosure:
#     def __init__(self, name, code, id, time, title):
#         self.name = name
#         self.code = code
#         self.id = id
#         self.time = time
#         self.title = title
#
#     def contruct_download_url(self):
#         url = 'http://three.cninfo.com.cn/new/announcement/download?bulletinId' \
#               f'={self.id}&announceTime={self.time}'
#         return url
#
#     def __repr__(self):
#         return str(self.__dict__)
#
#
#
# def query_company_disclosure(browser, start_date):
#     url = 'http://three.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice-sse'
#     with ghost.start() as session:
#         page, extra_resources = session.open(url)
#         # session.show()
#         try:
#             session.wait_for(lambda: False, '', 1)
#         except:
#             pass
#         assert page.http_status == 200
#         # session.open('http://www.baidu.com')
#         pyval = pyquery.PyQuery(session.content)
#         pyval = pyval('#page-list')
#
#         pylist = [pyquery.PyQuery(item) for item in pyval('div.page-list')]
#         pylist = pylist[0:1]
#         return [extract_disclosure_info(item) for item in pylist]
#
# def try_download_company_disclosures(disclosure_list:List[Disclosure]):
#     for item in disclosure_list:
#         last_date =
#
#
# def download_company_disclosure(announce_item: Disclosure):
#     import os
#     path = ppath.announcement
#     isok = firefox_quick_download_file(announce_item.contruct_download_url(), path)
#     print('isok:: \n', isok)
#
#
#
# def extract_disclosure_info(item):
#     header = item('.page-list-header')
#     subname = header('.sub-name')
#     name = subname.text()
#
#     content = item('.page-list-list')
#     content_list = [pyquery.PyQuery(item) for item in content('.sub-notice-important.touch')]
#     list_announce = []
#     for item in content_list:
#         item = item('a')
#         url = item.attr('href')
#         urlparams = urllib.parse.urlparse(url).query
#         urlparams = urllib.parse.parse_qs(urlparams)
#         title = item.attr('title')
#         announce_item = Disclosure(name, urlparams['stockCode'], urlparams['announcementId'],
#                                    urlparams['announcementTime'], title)
#         list_announce.append(announce_item)
#     return list_announce
#
#
# query_company_disclosure(ghost)
