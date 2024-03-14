from django.urls import path, include


app_name = 'api'

urlpatterns = [
	path('news/', include('backend.api.articles.urls', namespace='news')),
	path('users/', include('backend.api.users.urls', namespace='users')),
]
