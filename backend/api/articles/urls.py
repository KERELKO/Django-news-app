from rest_framework import routers
from django.urls import path, include 

from . import views


app_name = 'news'

router = routers.DefaultRouter()
router.register(r'articles', views.ArticleViewSet)
router.register(r'topics', views.TopicViewSet)


# api:news:<view_name>
urlpatterns = [
	path('', include(router.urls)),
]
