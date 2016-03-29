"""
configs tagging related templatetags.
"""
from django import template
from django.utils.safestring import mark_safe
from tagging.models import Tag

register = template.Library()


@register.simple_tag()
def selectize_tags():
    """
    returns all tags
    """
    return mark_safe([{'value': t.name,
                       'text': t.name} for t in Tag.objects.all()])


