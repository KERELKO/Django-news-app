from typing import Type, Optional
from django.apps import apps
from django.forms import modelform_factory
from .exceptions import IncorrectModelNameError

MODELS = ['text', 'image', 'video']


def get_form(
	model: Type['Model'],
	data: Optional[dict] = None,
	instance: Optional['ModelForm'] = None,
	files: dict['str', Type['UploadedFile']] = None,
) -> Type['Form']:
	form_class = modelform_factory(
		model=model,
		fields='__all__'
	)
	return form_class(data=data, instance=instance, files=files)


def get_model(model_name: str) -> Optional[Type['Model']]:
	model = None
	if model_name in MODELS:
		model = apps.get_model(
			app_label='content',
			model_name=model_name
		)
		return model
	raise IncorrectModelNameError(model_name)
