from src.main.app import db

class NumberModel(db.Model):

    phone_number = db.Column(db.String(12), primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    spam = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Number(phone_number = {self.number}, description = {self.description}, spam = {self.spam})"


if __name__ == '__main__':
    db.create_all()