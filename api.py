#!birds/bin/python
from flask import Flask, make_response
from src.controllers.version import version_controller
from src.controllers.birds import get_birds_controller, post_birds_controller
from flask import request


app = Flask(__name__)


@app.route('/version')
def version():
    return version_controller()


@app.route('/birds', methods=['GET'])
def get_birds():
    return get_birds_controller(request.args)


@app.route('/birds', methods=['POST'])
def post_bird():
    return post_birds_controller(request.get_json())


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)