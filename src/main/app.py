

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from config import config


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_URI
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class NumberModel(db.Model):

    phone_number = db.Column(db.String(12), primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    spam = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Number(phone_number = {self.number}, description = {self.description}, spam = {self.spam})"


number_put_args = reqparse.RequestParser()
number_put_args.add_argument("description", type=str, help="Description of the number is required", required=True)
number_put_args.add_argument("spam", type=bool, help="Number is a spam", required=False, default=False)

number_update_args = reqparse.RequestParser()
number_update_args.add_argument("description", type=str, help="Description of the number is required")
number_update_args.add_argument("spam", type=bool, help="Number is a spam",)

resource_fields = {
	'phone_number': fields.String,
    'description': fields.String,
	'spam': fields.Boolean
}

class Number(Resource):

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
                             spam=args['spam'])
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
            number.views = args['description']
        if args['spam']:
            number.likes = args['spam']

        db.session.commit()

        return number


    def delete(self, phone_number):
        number = NumberModel.query.filter_by(phone_number=phone_number).first()
        if not number:
            abort(404, message="Could not find such phone number!")
        db.session.delete(number)
        db.session.commit()
        return 'Successfully deleted!', 204


api.add_resource(Number, "/api/number/<int:phone_number>")


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
    db.create_all()