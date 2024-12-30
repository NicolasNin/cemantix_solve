# app.py
from flask import Flask
from routes import main
from models import get_model

model = None

def create_app():
    app = Flask(__name__)
    
    with app.app_context():
        global model
        model = get_model()
    
    app.register_blueprint(main)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)