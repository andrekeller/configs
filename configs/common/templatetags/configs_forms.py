"""
confi.gs form template tags.
"""
# django
from django import template
from django.utils.safestring import mark_safe
# 3rd-party
from tagging.models import Tag

register = template.Library()


@register.simple_tag()
def selectize_tags():
    """
    returns all tags
    """
    return mark_safe([{'value': t.name,
                       'text': t.name} for t in Tag.objects.all()])
