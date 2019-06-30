#!/bin/env python3

import base64
import json
import logging
import os

import decouple
import requests
import sqlite3 as sql

import utils


# response from checker:
# {
#     "success": true,
#     "new": true,
#     "message": "https://www.sidnfonds.nl/wat-we-doen was added to the ledger",
#     "score": {
#         "fake": 0,
#         "normal": 1,
#         "good": 0
#     },
#     "screenshot": "https://f002.backblazeb2.com/file/crimebusterbot/sidnfonds-8a75.png"
# }


ACCESS_TOKEN = decouple.config('ACCESS_TOKEN')
ACCESS_URL = decouple.config('ACCESS_URL')
# FIXME: implement obtaining `api-key`
API_KEY = decouple.config('API_KEY')
CHECK_URL = decouple.config('CHECK_URL')
PASSWORD = decouple.config('PASSWORD')
Q_FILE_NAME = decouple.config('QUEUEING_URLS_FILE_NAME')
USERNAME = decouple.config('USERNAME')


class Queuer:
    '''Processes multiple urls through the checks.'''

    logger = logging.getLogger('cbb.queue')
    logger.setLevel(logging.DEBUG)

#    def __init__(self):
#        self.urls = self._read_urls_file(Q_FILE_NAME)

    def process_queue(self):

        with sql.connect('urls.db') as con:
            cur = con.cursor()
            cur.execute('SELECT url FROM url_table LIMIT 1')
            # fetchone() returns a tuple
            url = cur.fetchone()
            if not url:
                print('DB is empty')
                return

            try:
                cur.execute('DELETE FROM url_table WHERE url=\'' + url[0] + '\'')
                con.commit()
                print('Record successfully deleted')
            except sql.OperationalError:
                print('Rolling back deletion ...')
                cur.rollback()

            print('Checking %s' % url)
            score = self._get_score(url)
            if score:
                print('Score of {0} is {1}'.format(url[0], score))
            else:
                print('Error: Something is wrong', url[0], score)

        return

    def _get_score(self, url):
        data = {'url': url}
        headers = {
            'api-key': API_KEY,
            'x-access-token': self._get_access_token(),
            'content-type': 'application/json',
        }
        resp = requests.post(CHECK_URL,
                             data=json.dumps(data),
                             headers=headers)
        print('response: %s' % resp.json())
        if resp.status_code in (200, 201):
            score_dict = resp.json().get('score')
            # for this to work, the values must be numbers, not strings
            return max(score_dict.items(), key=lambda k: k[1])

        return

    def _get_access_token(self):
        # TODO: implement checking expiration date of the JWT
        data = {
            'username': USERNAME,
            'password': PASSWORD,
        }
        headers = {
            'api-key': API_KEY,
            'content-type': 'application/json',
        }
        resp = requests.post(ACCESS_URL,
                             data=json.dumps(data),
                             headers=headers)
        if resp.status_code in (200, 201):
            print('Obtained access token. Status code: {}'.format(
                resp.status_code))
            ACCESS_TOKEN = resp.json().get('token')
            return ACCESS_TOKEN

        print('Cannot obtain access token. Status code: {}'.format(
              resp.status_code))
        return
