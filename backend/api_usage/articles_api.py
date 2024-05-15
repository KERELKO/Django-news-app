from .utils import get_response_or_error


BASE_ARTICLE_URL = 'http://127.0.0.1:8000' + '/api/news/articles/'
BASE_TOPIC_URL = 'http://127.0.0.1:8000' + '/api/news/topics/'


def get_article_by_id(id: int) -> dict:
    url = BASE_ARTICLE_URL + str(id)
    response = get_response_or_error(url)
    return response.json()


def get_article_list() -> list[dict]:
    url = BASE_ARTICLE_URL
    response = get_response_or_error(url)
    return response.json()


def get_hyperlinked_article_list() -> list[dict]:
    url = BASE_ARTICLE_URL + 'hyperlinked/'
    response = get_response_or_error(url)
    return response.json()


def get_topic_list() -> list[dict]:
    url = BASE_TOPIC_URL
    response = get_response_or_error(url)
    return response.json()
