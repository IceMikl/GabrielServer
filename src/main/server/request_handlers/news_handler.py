
from flask import Blueprint
from sqlalchemy import and_

from src.main.phone_number_parser import PhoneNumberHandler
import src.main.database.database_manager as db_manager
from src.main.database.models import BlockedNumber, GivenNumberBlock, TellowsNumber

from src.main.datasources.datasource_manager import DatasourceManager

news = Blueprint('news', __name__)


@news.route('/get/sueddeutsche', methods=['GET'])
def get_news_from_sueddeutsche():
    datasource_manager = DatasourceManager()
    actual_news_json = datasource_manager.get_sueddeutsche_news(make_request=True)
    return actual_news_json, 200


d3c1be18dd09c7195e369336b6de2f3b7b6f843fbf2fa092190b

