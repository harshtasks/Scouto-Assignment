from flask import Flask

from app.api.routes import api

# Creating our flask app
def create_app():

    app = Flask(__name__)

    # registering all the blueprints
    app.register_blueprint(api)
    
    @app.route('/')
    def mainpage():
        return "Go to <a href='https://dbooks.harshio.repl.co/api' target='_blank'>https://dbooks.harshio.repl.co/api</a>"

    return app
