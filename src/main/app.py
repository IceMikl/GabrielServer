import sys

if("/" not in sys.path):
    sys.path.append("/")
print(sys.path)

from flask import Flask
#from flask_restful import Api

import src.main.database.database_manager as db_manager



app = Flask(__name__)
#api = Api(app)
#TODO: remove sqlalchemy from requirements.txt
#app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_URI
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

#import src.main.resource_handlers.number_resource_handler as number_resource_handler
#api.add_resource(number_resource_handler.NumberResourceHandler, "/api/number/<string:phone_number>")


@app.route('/api/number/<string:phone_number>', methods=['GET'])
def check_phone_number(phone_number):
    return {'phone_number': phone_number, 'suspicious': 7}, 200


'''
def initialize_database():
    print("initialize_database")
    db.drop_all()
    db.create_all()
    add_data_to_database()
'''

'''
def add_data_to_database():
    database_manager = db_manager.DatabaseManager(database=db)
    database_manager.add_data_from_bundesnetzagentur()
'''


def create_database():
    database_manager = db_manager.DatabaseManager()
    database_manager.add_bna_blocked_numbers()
    database_manager.add_bna_given_numbers()

def start_server():
    create_database()
    app.run(debug=True, use_reloader=False, port=8080, host="0.0.0.0")


if __name__ == "__main__":
    start_server()


