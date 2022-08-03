from flask import Flask

from app.api.routes import api

# Creating our flask app
def create_app():

    app = Flask(__name__)

    # registering all the blueprints
    app.register_blueprint(api)
    
    @app.route('/')
    def mainpage():
        return "Go to <a href='https://localhost:5000/api/find?term=in' target='_blank'>https://localhost:5000/api/find?term=in</a><br>See documentation <a href='https://github.com/harshtasks/Scouto-Assignment/blob/main/README.md' target='_blank'>https://github.com/harshtasks/Scouto-Assignment/blob/main/README.md</a>"

    return app
