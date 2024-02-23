from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('news/', include('apps.articles.urls', namespace='articles')),
    path('content/', include('apps.content.urls', namespace='content')),
    path('users/', include('apps.users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )