import os

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from config import config

from src.main.resource_handlers.number_resource_handler import NumberResourceHandler
from src.main.database.models import NumberModel

app = Flask(__name__)
api = Api(app)

'''
class Number(Resource):

    def get(self, phone_number):
        return {'spam': True}, 200

api.add_resource(Number, "/api/number/<int:phone_number>")

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
'''


app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api.add_resource(NumberResourceHandler, "/api/number/<int:phone_number>")


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True, port=8080, host="0.0.0.0")
    test_number_1 = NumberModel(phone_number='123', description='test number', spam=False)
    test_number_2 = NumberModel(phone_number='143', description='test number', spam=False)
    db.session.add(test_number_1)
    db.session.add(test_number_2)
    db.session.commit()

    print(NumberModel.query_all())
