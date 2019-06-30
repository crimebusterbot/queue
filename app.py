#!/usr/bin/env python3

import base64
import logging

import decouple
import requests
import sqlite3 as sql

from flask import g, jsonify, request
from flask_api import FlaskAPI
from flask_apscheduler import APScheduler

import utils
from queuer import Queuer


Q_FILE_NAME = decouple.config('QUEUEING_URLS_FILE_NAME')


app = FlaskAPI(__name__)


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'app:process_queue',
            'args': (),
            'trigger': 'interval',
            'seconds': 10,
        }
    ]
    SCHEDULER_API_ENABLED = True


@app.before_request
def before_request():
    # execute `sqlite3 urls.db < schema.sql` in terminal
    # to create a db file from the schema file,
    # if it does not exist
    g.db = sql.connect("urls.db")


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/api/v1/queuer/', methods=['POST'])
def get_urls():
    # checks for 'urls' key in json
    urls = request.data.get('urls')
    for url in urls:
        print('url: %s' % url)
        try:
            g.db.execute('INSERT INTO url_table VALUES (?)', (url,))
            g.db.commit()
        except sql.IntegrityError:
            print('Rolling back insertion ...')
            g.db.rollback()

    return jsonify({})


def process_queue():
    print('Running job ...')
    q = Queuer()
    q.process_queue()


if __name__ == '__main__':
    app.config.from_object(Config())

    scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5055,
    )
