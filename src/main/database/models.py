from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Sequence


class BaseModel:

    BASE = declarative_base()


class BlockedNumber(BaseModel.BASE):
    __tablename__ = 'BlockedNumber'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    phone_number = Column(String)
    description = Column(String)
    suspicious = Column(Integer)

    def __repr__(self):
        return f'<BlockedNumber(id={self.id}, phone_number={self.phone_number}, ' \
               f'description={self.description}, suspicious={self.suspicious})>'



