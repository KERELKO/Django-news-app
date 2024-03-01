from django.http import HttpResponse


class AuthorMixin:
	"""
	Mixin to restrict access based on the author of an object
	Model must have 'author'(ForeignKey) field to use this mixin
	"""
	def dispatch(self, request, *args, **kwargs):
		if request.user != self.get_object().author or not request.user.is_staff:
			return HttpResponse('You don\'t have permissions') 
		return super().dispatch(request, *args, **kwargs)
