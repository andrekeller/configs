import json
from django.forms.widgets import Widget, TextInput
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe


class EncdataWidget(Widget):

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.encdata_fields = settings.ENCDATA_FIELDS

    def render(self, name, value, attrs=None):
        try:
            value_dict = json.loads(value)
        except TypeError:
            value_dict = {}

        html = []
        final_attrs = self.build_attrs(attrs)
        for encdata_field in self.encdata_fields:
            field_name = '%s_%s' % (name, encdata_field)
            field_id = 'id_%s' % field_name
            field_value = value_dict.get(encdata_field, '')
            field_attrs = dict(final_attrs, id=field_id)
            html += [
                '<div class="input-group form-spacer">',
                '<span class="input-group-addon">{}</label></span>'.format(
                    encdata_field
                ),
                TextInput(attrs=attrs).render(field_name,
                                              force_text(field_value),
                                              field_attrs),
                '</div>',
            ]
        return mark_safe('\n'.join(html))

    def value_from_datadict(self, data, files, name):
        value = {}
        for encdata_field in self.encdata_fields:
            field_name = '%s_%s' % (name, encdata_field)
            field_value = data.get(field_name, None)
            if field_value:
                value[encdata_field] = field_value
        return json.dumps(value)
