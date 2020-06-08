from django import template
from django import templatetags

register = template.Library()

from ..models import Chat


@register.simple_tag
def get_companion(user, chat):
    for u in chat.members.all():
        if u != user.profile:
            return u
    return None
