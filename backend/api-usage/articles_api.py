import os
import asyncio 
import httpx
from dotenv import load_dotenv

load_dotenv()
DOMAIN = os.getenv('DOMAIN')


async def get_articles_list(url: str) -> dict | list[dict]:
	async with httpx.AsyncClient() as client:
		response = await client.get(url)
		if response.is_redirect:
			redirect_url = response.headers['location']
			response = await client.get(DOMAIN + redirect_url)
	return response.json()


async def main() -> None:
	url = f'{DOMAIN}/api/news/articles/'
	response = await get_articles_list(url)
	print(response)


if __name__ == '__main__':
	asyncio.run(main())
