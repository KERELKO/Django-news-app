from django.urls import path
from . import views


app_name = 'content'

urlpatterns = [
    path(
        'create/<int:article_id>/<str:model_name>/',
        views.CreateContentView.as_view(),
        name='create',
    ),
    path(
        'edit/<int:article_id>/<str:model_name>/<int:content_id>/',
        views.EditContentView.as_view(),
        name='edit',
    ),
    path(
        'delete/<int:article_id>/<int:content_id>',
        views.DeleteContentView.as_view(),
        name='delete',
    ),
]
