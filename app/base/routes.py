from crypt import methods
from app.base import blueprint
from flask import render_template


@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('index.html')


@blueprint.route("/nlp", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"
