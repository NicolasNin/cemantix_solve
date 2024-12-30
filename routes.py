from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Hello World"

@main.route('/analyze')
def analyze():
    return "Analysis route"