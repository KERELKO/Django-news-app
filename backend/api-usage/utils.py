from typing import Type

import requests


def get_response_or_error(url: str, timeout=5, **kwargs) -> Type['Response']:
	try:  
		response = requests.get(
			url, 
			timeout=timeout,
			**kwargs
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
	return response
