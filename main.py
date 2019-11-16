from flask import Flask 
from flask_restful import Api

from api import TopWords, Users, Mentions, Hourly


app = Flask(__name__)
api = Api(app)

api.add_resource(TopWords, '/topwords')
api.add_resource(Users, '/popular/users')
api.add_resource(Mentions, '/popular/mentions')
api.add_resource(Hourly, '/hourly')

@app.route('/')
def home():
    return('good eve')


if __name__ == '__main__':
    app.run(debug=True)