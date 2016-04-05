from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.forms import ModelForm


class ParentModelForm(ModelForm):
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