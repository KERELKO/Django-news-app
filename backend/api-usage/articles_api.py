import os
import requests
from dotenv import load_dotenv

from utils import get_response_or_error

load_dotenv()
DOMAIN = os.environ.get('DOMAIN')

BASE_ARTICLE_URL = DOMAIN + '/api/news/articles/'
BASE_TOPIC_URL = DOMAIN + '/api/news/topics/'


def get_article_by_id(id: int) -> dict:
	url = BASE_ARTICLE_URL + f'{id}'
	response = get_response_or_error(url)
	return response.json()


def get_article_list() -> list[dict]:
	url = BASE_ARTICLE_URL
	response = get_response_or_error(url)
	return response.json()


def get_hyperlinked_article_list() -> list[dict]:
	url = BASE_ARTICLE_URL + 'hyperlinked/'
	try:  
		response = requests.get(
			url, 
			timeout=5
		)
		response.raise_for_status()
	except requests.Timeout as ex:
		raise requests.Timeout(
			f'Timeout error occurred: Request took longer than the specified' 
			f'timeout period, url: {url}'
		) from ex
	except requests.HTTPError as ex:
		raise requests.HTTPError(
			f'HTTP error occurred while getting response from: {url}'
		) from ex
	return response.json()


def get_topic_list() -> list[dict]:
	url = BASE_TOPIC_URL
	try:
		response = requests.get(
			url,
			timeout=5
		)
		response.raise_for_status()
	except requests.Timeout as ex:
		raise requests.Timeout(
			f'Timeout error occurred: Request took longer than the specified' 
			f'timeout period, url: {url}'
		) from ex
	except requests.HTTPError as ex:
		raise requests.HTTPError(
			f'HTTP error occurred while getting response from: {url}'
		) from ex
	return response.json()
	

print(get_article_list())
