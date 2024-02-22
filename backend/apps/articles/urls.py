from django.urls import path  
from . import views  


app_name = 'articles'

urlpatterns = [
	path(
		'', 
		views.ArticleListView.as_view(), 
		name='list'
	),
	path(
		'topic/<slug:topic_slug>/', 
		views.ArticleListView.as_view(),
		name='list_topic'
	),
	path(
		'detail/<slug:slug>/<int:year>/<int:month>/<int:day>/',
		views.ArticleDetailView.as_view(),
		name='detail'
	),
	path(
		'edit/<pk>/', 
		views.ArticleEditView.as_view(),
		name='edit'
	),
	path(
		'create/', 
		views.ArticleCreateView.as_view(),
		name='create'
	),
	path(
		'delete/<pk>/', 
		views.ArticleDeleteView.as_view(),
		name='delete'
	),
	path(
		'comment/delete/<pk>/',
		views.CommentDeleteView.as_view(),
		name='comment_delete',
	),
	path(
		'comment/edit/<pk>/',
		views.CommentEditView.as_view(),
		name='comment_edit',
	)
]
