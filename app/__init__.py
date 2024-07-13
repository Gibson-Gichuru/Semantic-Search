from flask import Flask
from config import environment

def create_app(config:str):

    app = Flask(__name__)
    
    app.config.from_object(environment[config])

    environment[config].init_app(app)

    from app.main import main_bp
    app.register_blueprint(main_bp)

    return app