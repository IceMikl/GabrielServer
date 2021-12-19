import os
import sys
sys.path.append("/")
print(sys.path)

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

import src.main.database.database_manager as db_manager

from config import config


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# See important note below
#from src.main.database.models import NumberModel

class NumberModel(db.Model):

    phone_number = db.Column(db.String(12), primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    suspicious = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Number(phone_number = {self.phone_number}, description = {self.description}, suspicious = {self.suspicious})"


from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
number_put_args = reqparse.RequestParser()
number_put_args.add_argument("description", type=str, help="Description of the number is required", required=True)
number_put_args.add_argument("suspicious", type=int, help="Number is a suspicious", required=False, default=False)

number_update_args = reqparse.RequestParser()
number_update_args.add_argument("description", type=str, help="Description of the number is required")
number_update_args.add_argument("suspicious", type=int, help="Number is suspicious",)

resource_fields = {
	'phone_number': fields.String,
    'description': fields.String,
	'suspicious': fields.Integer
}

class NumberResourceHandler(Resource):

    @marshal_with(resource_fields)
    def get(self, phone_number):
        result = NumberModel.query.filter_by(phone_number=phone_number).first()
        if not result:
            abort(404, message="Could not find such phone number!")
        return result

    @marshal_with(resource_fields)
    def put(self, phone_number):
        args = number_put_args.parse_args()
        number = NumberModel.query.filter_by(phone_number=phone_number).first()
        if number:
            abort(409, message="Phone number already exists!")

        number = NumberModel(phone_number=phone_number, description=args['description'],
                             suspicious=args['suspicious'])
        db.session.add(number)
        db.session.commit()
        return number, 201

    @marshal_with(resource_fields)
    def update(self, phone_number):
        args = number_update_args.parse_args()
        number = NumberModel.query.filter_by(phone_number=phone_number).first()
        if not number:
            abort(404, message="Phone number doesn't exist, cannot update")

        if args['description']:
            number.description = args['description']
        if args['suspicious']:
            number.suspicious = args['suspicious']

        db.session.commit()

        return number

    def delete(self, phone_number):
        number = NumberModel.query.filter_by(phone_number=phone_number).first()
        if not number:
            abort(404, message="Could not find such phone number!")
        db.session.delete(number)
        db.session.commit()
        return 'Successfully deleted!', 204


#from src.main.resource_handlers.number_resource_handler import NumberResourceHandler

api.add_resource(NumberResourceHandler, "/api/number/<string:phone_number>")


def initialize_database():
    print("initialize_database")
    db.drop_all()
    db.create_all()
    add_data_to_database()


def add_data_to_database():
    '''
    test_number_1 = NumberModel(phone_number='10', description='test number', suspicious=5)
    test_number_2 = NumberModel(phone_number='11', description='test number', suspicious=5)
    db.session.add(test_number_1)
    db.session.add(test_number_2)
    db.session.commit()
    print(NumberModel.query.all())
    '''
    print("add_data_to_database")
    database_manager = db_manager.DatabaseManager(database=db)
    database_manager.add_data_from_bundesnetzagentur()
    #print(NumberModel.query.all())



if __name__ == "__main__":
    print("__name__")
    print(os.listdir("."))
    initialize_database()
    app.run(debug=True, use_reloader=False, port=8080, host="0.0.0.0")

