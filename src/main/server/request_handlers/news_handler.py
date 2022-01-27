
from flask import Blueprint

from src.main.datasources.datasource_manager import DatasourceManager

news = Blueprint('news', __name__)


@news.route('/get/sueddeutsche', methods=['GET'])
def get_news_from_sueddeutsche():
    """Endpoint to get news from Sueddeutsche Zeitung
        This endpoint get news related to "Telefonbetrug" from Sueddeutsche RSS
        ---
        definitions:
            SuedeutscheZeitungRss:
                type: object
                properties:
                    rss:
                        $ref: '#/definitions/RssFeed'
            RssFeed:
                type: object
                properties:
                    "@version":
                        type: string
                    "@xmlns:atom":
                        type: string
                    channel:
                        $ref: '#/definitions/Channel'
            Channel:
                type: object
                properties:
                    "atom:link":
                        $ref: '#/definitions/AtomLink'
                    title:
                        type: string
                    link:
                        type: string
                    description:
                        type: string
                    pubDate:
                        type: string
                    managingEditor:
                        type: string
                    language:
                        type: string
                    image:
                        $ref: '#/definitions/Image'
                    pubDate:
                        type: string
                    item:
                        type: array
                        items:
                            $ref: '#/definitions/Item'
            AtomLink:
                type: object
                properties:
                    "@href":
                        type: string
                    "@rel":
                        type: string
                    "@type":
                        type: string
            Image:
                type: object
                properties:
                    url:
                        type: string
                    title:
                        type: string
                    link:
                        type: string
                    width:
                        type: string
                    height:
                        type: string
            Item:
                type: object
                properties:
                    link:
                        type: string
                    title:
                        type: string
                    description:
                        type: string
                    guid:
                        type: string
                    pubDate:
                        type: string
        responses:
            200:
                description: Returns Sueddeutsche Zeitung RSS feeds.
                schema:
                    $ref: '#/definitions/SuedeutscheZeitungRss'
    """
    datasource_manager = DatasourceManager()
    actual_news_json = datasource_manager.get_sueddeutsche_news(make_request=True)
    return actual_news_json, 200



@news.route('/get/faz', methods=['GET'])
def get_news_from_faz():
    """Endpoint to get news from Frankfurter Allgemeine Zeitung
        This endpoint get news related to "gesellschaft/kriminalitaet/" from Frankfurter Allgemeine Zeitung RSS
        ---
        definitions:
            fazRss:
                type: object
                properties:
                    rss:
                        $ref: '#/definitions/RssFeed'
            RssFeed:
                type: object
                properties:
                    "@version":
                        type: string
                    "@xmlns:atom":
                        type: string
                    "@xmlns:media":
                        type: string
                    channel:
                        $ref: '#/definitions/Channel'
            Channel:
                type: object
                properties:
                    "atom:link":
                        $ref: '#/definitions/AtomLink'
                    category:
                        type: string
                    copyright:
                        type: string
                    description:
                        type: string
                    docs:
                        type: string
                    generator:
                        type: string
                    image:
                        $ref: '#/definitions/Image'
                    item:
                        type: array
                        items:
                            $ref: '#/definitions/Item'
                    language:
                        type: string
                    lastBuildDate:
                        type: string
                    link:
                        type: string
                    title:
                        type: string
                    ttl:
                        type: string
            AtomLink:
                type: object
                properties:
                    "@href":
                        type: string
                    "@rel":
                        type: string
                    "@type":
                        type: string
            Image:
                type: object
                properties:
                    link:
                        type: string
                    title:
                        type: string
                    url:
                        type: string
            Item:
                type: object
                properties:
                    link:
                        type: string
                    title:
                        type: string
                    description:
                        type: string
                    guid:
                        type: string
                    pubDate:
                        type: string
        responses:
            200:
                description: Returns Sueddeutsche Zeitung RSS feeds.
                schema:
                    $ref: '#/definitions/SuedeutscheZeitungRss'
    """
    datasource_manager = DatasourceManager()
    actual_news_json = datasource_manager.get_faz_news(make_request=True)
    return actual_news_json, 200




