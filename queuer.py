#!/bin/env python3

import base64
import logging

import decouple
import requests


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


USERNAME = decouple.config('USERNAME')
PASSWORD = decouple.config('PASSWORD')


class Queuer:
    '''Processes multiple urls through the checks.'''

    logger = logging.getLogger('cbb.queue')
    logger.setLevel(logging.DEBUG)

    def __init__(self, urls):
        self.urls = urls
        self.check_url = 'https://webshop-checker.nl/webshop/check/'

    def process_queue(self):
        for url in self.urls:
            print('Checking %s' % url)
            check = self._check_webshop(url)
            if check:
                print('Check successful')
            else:
                print('Error: Something is wrong')

        return

    def _check_webshop(self, url):
        data = {'url': url}
        resp = requests.post(self.check_url,
                             data=data,
                             headers=self._set_headers())
        print('Get status code from checker: %s' % resp.status_code)
        if resp.status_code in (200, 201):
            print('Response from checker: %s' % resp.json())
            return True

        return

    def _set_headers(self):
        login_b64 = base64.b64encode(
            '{}:{}'.format(USERNAME, PASSWORD).encode('utf-8'))
        return {'Authorization': 'Basic {}'.format(login_b64)}
