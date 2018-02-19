from datetime import datetime, timedelta
from django import template
from django.utils.timesince import timesince
from django.utils import timezone

register = template.Library()

@register.filter
def age(value):
    now = timezone.now()
    try:
        difference = now - value
    except:
        return value

    if difference <= timedelta(minutes=1):
        return 'Just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}
