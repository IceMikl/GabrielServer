
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

import src.main.database.models as db_models
from src.main.app import db


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
        result = db_models.NumberModel.query.filter_by(phone_number=phone_number).first()
        if not result:
            abort(404, message="Could not find such phone number!")
        return result

    @marshal_with(resource_fields)
    def put(self, phone_number):
        args = number_put_args.parse_args()
        number = db_models.NumberModel.query.filter_by(phone_number=phone_number).first()
        if number:
            abort(409, message="Phone number already exists!")

        number = db_models.NumberModel(phone_number=phone_number, description=args['description'],
                             suspicious=args['suspicious'])
        db.session.add(number)
        db.session.commit()
        return number, 201

    @marshal_with(resource_fields)
    def update(self, phone_number):
        args = number_update_args.parse_args()
        number = db_models.NumberModel.query.filter_by(phone_number=phone_number).first()
        if not number:
            abort(404, message="Phone number doesn't exist, cannot update")

        if args['description']:
            number.description = args['description']
        if args['suspicious']:
            number.suspicious = args['suspicious']

        db.session.commit()

        return number

    def delete(self, phone_number):
        number = db_models.NumberModel.query.filter_by(phone_number=phone_number).first()
        if not number:
            abort(404, message="Could not find such phone number!")
        db.session.delete(number)
        db.session.commit()
        return 'Successfully deleted!', 204

