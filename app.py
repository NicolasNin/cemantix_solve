# app.py
from flask import Flask
from routes import main
from solver import Solver
from solver import Game

def create_app():
    app = Flask(__name__)
    app.config['SOLVER'] = Solver()
    app.config['GAME'] = Game(app.config['SOLVER'].model)
    app.register_blueprint(main)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)