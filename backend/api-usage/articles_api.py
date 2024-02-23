import asyncio 
import httpx


async def get_articles_list(url: str) -> dict:
	async with httpx.AsyncClient() as client:
		response = await client.get(url)
		if response.is_redirect:
			redirect_url = response.headers['location']
			response = await client.get('http://127.0.0.1:8000' + redirect_url)
	print(response.json())


async def main() -> None:
	url = 'http://127.0.0.1:8000/api/news/articles/6?format=json'
	await get_articles_list(url)


if __name__ == '__main__':
	asyncio.run(main())
