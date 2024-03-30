from typing import Optional, Type, Any

from django.apps import apps
from django.db.models import Model
from django.forms import modelform_factory, ModelForm, Form
from django.core.files.uploadedfile import UploadedFile

from .exceptions import IncorrectModelNameError


ALLOWED_MODELS = ['text', 'image', 'video']


def get_form(
    model: Type[Model],
    data: Optional[dict[str, Any]] = None,
    instance: Optional[ModelForm] = None,
    files: Optional[dict[str, UploadedFile]] = None,
) -> Form:
    """Function to get form for the model"""
    form_class = modelform_factory(model=model, fields='__all__')
    return form_class(data=data, instance=instance, files=files)


def get_model(model_name: str) -> Model:
    """
    Function to get model that appears in 'ALLOWED_MODELS'
    and related to 'content' app,
    if name of the model is incorrect raises 'IncorrectModelNameError'
    """
    model = None
    if model_name.lower() in ALLOWED_MODELS:
        model = apps.get_model(
            app_label='content', model_name=model_name.lower()
        )
        return model
    raise IncorrectModelNameError(model_name, ALLOWED_MODELS)
