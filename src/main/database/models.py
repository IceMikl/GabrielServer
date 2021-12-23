
'''
import src.main.app as app

class NumberModel(app.db.Model):

    phone_number = app.db.Column(app.db.String(12), primary_key=True)
    description = app.db.Column(app.db.String(500), nullable=False)
    suspicious = app.db.Column(app.db.Integer, nullable=False)

    def __repr__(self):
        return f"Number(phone_number = {self.phone_number}, description = {self.description}, suspicious = {self.suspicious})"

'''

