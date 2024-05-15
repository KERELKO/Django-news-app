APP = django-news-app-web-1
EXEC = docker exec -it
MANAGE = ${APP} python manage.py

.PHONY: bash
bash:
	${EXEC} ${APP} bash

.PHONY: migrate
migrate:
	${EXEC} ${MANAGE} migrate
