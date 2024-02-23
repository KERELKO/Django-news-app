from django.urls import path, include


app_name = 'api'

urlpatterns = [
	path('news/', include('api.articles.urls')),
	path('users/', include('api.users.urls')),
]
