from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from . import tasks


class AuthorMixin:
	"""
	Mixin to restrict access based on the author of an object
	Model must have 'author'(ForeignKey) field to use this mixin
	"""
	def dispatch(self, request, *args, **kwargs):
		if request.user != self.get_object().author and not request.user.is_staff:
			return HttpResponse('You don\'t have permissions') 
		return super().dispatch(request, *args, **kwargs)


class TaskMixin:
	task_name = None

	def get_task(self):
		return self.task_name

	def dispatch(self, request, *args, **kwargs):
		if not self.task_name:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} is missing the "
				f"task_name attribute. Define "
				f"{self.__class__.__name__}.task_name or override"
				f"get_task method"
			)
		tasks.self.get_task(*args, **kwargs)
