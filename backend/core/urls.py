from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('users/', include('backend.apps.users.urls', namespace='users')),
    path('api/', include('backend.api.urls', namespace='api')),
    path('news/', include('backend.apps.articles.urls', namespace='articles')),
    path('content/', include('backend.apps.content.urls', namespace='content')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
