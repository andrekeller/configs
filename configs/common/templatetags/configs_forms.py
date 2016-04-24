"""
confi.gs form template tags.
"""
# django
from django import template
from django.utils.safestring import mark_safe
# 3rd-party
from tagging.models import Tag

register = template.Library()


@register.filter()
def add_class(field, class_name):
    """
    adds a css class to a django form widget
    """
    # TODO: add test
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name))
    })


@register.simple_tag()
def selectize_tags():
    """
    returns all tags
    """
    # TODO: add test
    return mark_safe([{'value': t.name,
                       'text': t.name} for t in Tag.objects.all()])
