# Django News App

## The Django News App offers a range of features to deliver and interact with news content. Here are some of its main functionalities:
- Watching news
- Create news
- Add comments to the news
- Search for the news
- Pick interesting topics
- Follow for the most popular news

### About other functions
Redis enhances the app's view system, allowing users to influence the popularity of news by increasing their view rate.  
Additionally, Redis is utilized for caching, optimizing the app's performance.  
Celery facilitates asynchronous task execution, enabling users to receive notifications about news updates via email.  
The Django Rest Framework empowers the app with a robust API, which can be easily tested using the [requests](https://requests.readthedocs.io/en/latest/) library.    
Furthermore, the app offers the flexibility to create diverse content formats for news articles, including videos, text, and images.    

## Technologies 
1. [Django](https://www.djangoproject.com/)
2. [Postgresql](https://www.postgresql.org/)
3. [Docker](https://www.docker.com/)
4. [Redis](https://redis.io/)
5. [Celery](https://docs.celeryq.dev/en/stable/)
6. [DRF](https://www.django-rest-framework.org/)

## How to install
You can install project with  
`git clone https://github.com/KERELKO/Django-news-app`  
To use all features of the project you can use docker compose  
`docker compose up`  
If you are using docker compose, then project works in production mode, where DEBUG=False,   
if you want to change it, you can do it directly in settings.prod or in docker-compose.yaml  

## About improvements
The main aspect that can be improved in this project is the frontend.  
For me, this project is interesting only in the backend, so maybe I will never write frontend for it.  
But there are a lot of different parts in the backend where it can be improved:
- Content order  
If you added huge text content for the news and previously added other content like videos or images, you can't put this text above them the only way is to delete it and rewrite it like new content 
- Better query optimization  
Some queries can be optimized to make fewer requests to the database  
- Better auth system and security  
Despite the fact that I created basic auth system and security for production it's obiously not enough. Users must have the ability to update their password, their profile etc.
- API
