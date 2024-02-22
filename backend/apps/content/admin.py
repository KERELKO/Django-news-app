from django.contrib import admin
from .models import(
	Content, 
	Text, 
	Video, 
	Image
)


admin.site.register(Content)
admin.site.register(Text)
admin.site.register(Image)
admin.site.register(Video)
