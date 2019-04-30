#!/usr/bin/env python3

from flask_api import FlaskAPI, jsonify

from .queue import Queuer


app = FlaskAPI(__name__)


@app.route("/api/v1/queue", methods=['POST'])
def queue():
    urls = request.get_json()
    q = Queuer(urls)
    q.process_queue()
    return jsonify({})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5055)
