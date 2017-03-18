from __future__ import print_function, division
from bs4 import BeautifulSoup as BS
from collections import defaultdict
import requests
import re
import simplejson as json
import os
import pickle

class SessionGoogle:
    def __init__(self, url_login, url_auth, login, pwd):
        self.ses = requests.session()
        login_html = self.ses.get(url_login)
        soup_login = BS(login_html.content).find('form').find_all('input')
        my_dict = {}
        for u in soup_login:
            if u.has_attr('value'):
                my_dict[u['name']] = u['value']
        # override the inputs without login and pwd:
        my_dict['Email'] = login
        my_dict['Passwd'] = pwd
        if not os.path.exists('../res/cookies'):
            with open('../res/cookies', 'wb') as fp:
                pickle.dump(self.ses.cookies, fp)
#        else:
#            with open('../res/cookies', 'rb') as fp:
#                self.ses.cookies = pickle.load(fp)
        self.ses.post(url_auth, data=my_dict)

    def get(self, URL):
        headers = {"Accept-Encoding": "identity"}
        self.resp = self.ses.get(URL, headers=headers)

    def get_page_text(self):
        self.text = self.resp.text.encode("utf-8")
        self.text = self.text.decode("string_escape")

    def parse_json(self):
        beg = self.text.rfind("JSON.parse(")+len("JSON.parse(")+1
        end = self.text.rfind("]")+1
        buf = self.text[beg:end]
        self.buf = buf
        notes = json.loads(buf)
        self.notedict = defaultdict(dict)
        for e in notes:
            if e['type'] == 'LIST':
                self.notedict[e['id']] = {'title': e['title']
                                          }
            elif e['type'] == 'LIST_ITEM':
                prt = self.notedict[e['parentId']].get('text')
                if prt is None:
                    prt = ''
                self.notedict[e['parentId']]['text'] = e['text'] + ' \n ' \
                    + prt
            elif e['type'] == 'NOTE':
                self.notedict[e['id']] = {'title': e['title'],
                                          'text': e['text']}
            if e['reminders'] != []:
                self.notedict[e['id']]['due'] = e['reminders'][0]['due']

    def get_reminders(self):
        reminders = []
        for k, v in self.notedict.iteritems():
            if 'due' in v.keys():
                dt = v['due']
                date = str(dt['year']) + str(dt['month']) + str(dt['day'])
                if v.get('text') is not None:
                    reminders.append([date, [v['title']] + v.get('text').strip(' ').split('\n')])
                else:
                    reminders.append([date, [v['title']]])
        return reminders

