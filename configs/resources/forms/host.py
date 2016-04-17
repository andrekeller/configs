from ..models import Host, Domain
from .widgets import EncdataWidget
from .mixins import ParentModelForm


class HostForm(ParentModelForm):
    parent_model = Domain

    class Meta:
        model = Host
        fields = [
            'name',
            'domain',
            'tags',
            'encdata',
        ]
        widgets = {
            'encdata': EncdataWidget(),
        }
