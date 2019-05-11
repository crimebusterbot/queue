#!/usr/bin/env python3

import base64
import logging

import requests

from flask_api import FlaskAPI
from flask import jsonify, request

from queuer import Queuer


app = FlaskAPI(__name__)


@app.route("/api/v1/queuer/", methods=['POST'])
def process_queue():
    # checks for 'urls' key in json
    urls = request.data
    q = Queuer(urls)
    q.process_queue()
    return jsonify({})


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5055,
    )
