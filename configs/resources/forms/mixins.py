"""
confi.gs resources form mixins
"""
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.forms import ModelForm


class ParentModelForm(ModelForm):
    """
    mixin for a form with models that have parents.

    this is used to provide sane defaults for related form fields, if forms
    represent hierichal models.
    """
    parent_model = None

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None

        if self.parent_model is None:
            raise ImproperlyConfigured(
                'Need to pass parent_model to ParentModelForm'
            )

        try:
            self.parent = self.parent_model.objects.get(id=parent)
        except ObjectDoesNotExist:
            pass
        else:
            self.fields[self.parent_model.__name__.lower()].initial = self.parent