from flask import Flask
from flask_restful import Api
from Users import Users
from Locations import Locations

app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')  # add endpoints
api.add_resource(Locations, '/locations')

if __name__ == '__main__':
    app.run()  # run our Flask app
