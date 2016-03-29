from django import forms
from django.core.exceptions import ObjectDoesNotExist
from ..models import Host, Domain
from .widgets import EncdataWidget


class HostForm(forms.ModelForm):

    def __init__(self, domain=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = None
        try:
            self.domain = Domain.objects.get(id=domain)
        except ObjectDoesNotExist:
            pass

        if self.domain:
            self.fields['domain'].initial = self.domain

    class Meta:
        model = Host
        fields = [
            'name',
            'domain',
            'tags',
            'encdata'
        ]
        widgets = {
            'encdata': EncdataWidget(),
        }
