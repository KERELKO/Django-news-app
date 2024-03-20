from django.core.exceptions import PermissionDenied


class AuthorMixin:
    """
    Mixin to restrict access based on the author of an object,
    the model must have an 'author' field(ForeignKey) to use this mixin
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().author and not request.user.is_staff:
            raise PermissionDenied('You don\'t have permissions')
        return super().dispatch(request, *args, **kwargs)
