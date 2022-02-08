from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Sequence


class BaseModel:
    BASE = declarative_base()



class BlockedNumber(BaseModel.BASE):
    __tablename__ = 'BLOCKED_NUMBER'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    phone_number = Column(String)
    description = Column(String)
    suspicious = Column(Integer)

    def __repr__(self):
        return f'<BlockedNumber(id={self.id}, phone_number={self.phone_number}, ' \
               f'description={self.description}, suspicious={self.suspicious})>'


class GivenNumberBlock(BaseModel.BASE):
    __tablename__ = 'GIVEN_NUMBER_BLOCK'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    area_code = Column(Integer)
    phone_block_from = Column(Integer)
    phone_block_to = Column(Integer)
    place_name = Column(String)
    phone_provider = Column(String)

    def __repr__(self):
        return f'<GivenNumberBlock(id={self.id}, area_code={self.area_code} ' \
               f'phone_block_from={self.phone_block_from}, phone_block_to={self.phone_block_to}, ' \
               f'place_name={self.place_name}, phone_provider={self.phone_provider})>'


class TellowsNumber(BaseModel.BASE):
    __tablename__ = 'TELLOWS_NUMBER'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    number = Column(String)
    score = Column(Integer)
    complains = Column(Integer)
    country = Column(Integer)
    prefix = Column(Integer)
    searches = Column(Integer)
    caller_type = Column(String)
    caller_name = Column(String)
    last_comment = Column(String)
    deeplink = Column(String)
    caller_typeid = Column(Integer)

    def __repr__(self):
        return f'<TellowsNumber(id={self.id}, number={self.number} score={self.score}, ' \
               f'complains={self.complains}, country={self.country}, prefix={self.prefix}, ' \
               f'searches={self.searches}, caller_type={self.caller_type}, caller_name={self.caller_name},' \
               f' last_comment={self.last_comment}, deeplink={self.deeplink}, caller_typeid={self.caller_typeid})>'



class AreaCode(BaseModel.BASE):
    __tablename__ = 'AREA_CODE'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    code = Column(Integer)
    place_name = Column(String)
    activ = Column(Integer)
    country = Column(String)

    def __repr__(self):
        return f'<AreaCode(id={self.id}, code={self.code}, place_name={self.place_name}, ' \
               f'activ={self.activ}, country={self.country})>'



class Request(BaseModel.BASE):
    __tablename__ = 'REQUEST'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)

    remote_addr = Column(String)
    base_url = Column(String)
    content_encoding = Column(String)
    content_type = Column(String)
    date = Column(String)
    data = Column(String)
    full_path = Column(String)
    headers = Column(String)
    host = Column(String)
    host_url = Column(String)
    path = Column(String)
    remote_user = Column(String)
    scheme = Column(String)
    url = Column(String)
    url_charset = Column(String)
    url_root = Column(String)
    url_rule = Column(String)
    user_agent = Column(String)
    request_time = Column(String)


    def __repr__(self):
        return f'<REQUEST(id={self.id}, remote_addr={self.remote_addr}, base_url={self.base_url}, ' \
               f'content_encoding={self.content_encoding}, content_type = {self.content_type}, date = {self.date}, ' \
               f'data={self.data}, full_path = {self.full_path}, headers = {self.headers}, ' \
               f'host={self.host}, host_url = {self.host_url}, path = {self.path}, ' \
               f'remote_user={self.remote_user}, scheme = {self.scheme}, url = {self.url}, ' \
               f'url_charset={self.url_charset}, url_root = {self.url_root}, url_rule = {self.url_rule}, ' \
               f'user_agent={self.user_agent}, request_time = {self.request_time})>'

