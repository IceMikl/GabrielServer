
from db_manager.src.main.datasources.news.faz_news_api import FazNewsApi




faz_news_api = FazNewsApi()


def test_make_request():
    print(faz_news_api.make_request())


def test_get_news_true():
    print(faz_news_api.get_news(make_request=True))


def test_get_news_false():
    print(faz_news_api.get_news(make_request=False))


if __name__ == '__main__':
    #test_make_request()
    #test_get_news_true()
    test_get_news_false()