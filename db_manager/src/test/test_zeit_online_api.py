
from db_manager.src.main.datasources.news.zeit_online_news_api import ZeitOnlineApi


def test_get_news(keyword='test'):
    zeit_online_api = ZeitOnlineApi()
    print(zeit_online_api.make_request(keyword=keyword))




if __name__ == '__main__':
    test_get_news(keyword='Test')