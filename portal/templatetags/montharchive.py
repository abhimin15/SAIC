from portal.models import *
from datetime import datetime, timedelta
from django import template
from django.utils.timesince import timesince
from django.utils import timezone
register = template.Library()


class FooNode(template.Node):

    def __init__(self, obj):
        # saves the passed obj parameter for later use
        # this is a template.Variable, because that way it can be resolved
        # against the current context in the render method
        self.object = template.Variable(obj)

    def render(self, context):
        # resolve allows the obj to be a variable name, otherwise everything
        # is a string
        obj = self.object.resolve(context)
        # obj now is the object you passed the tag
        '''Recieves each row from a query and
        return the Who_requested user's information
        '''
        month_name=obj
        year = 2016
        if month_name == "January":
            month=1
        if month_name == "February":
            month=2
        if month_name == "March":
            month=3
        if month_name == "April":
            month=4
        if month_name == "May":
            month=5
        if month_name == "June":
            month=6
        if month_name == "July":
            month=7
        if month_name == "August":
            month=8
        if month_name == "September":
            month=9
        if month_name == "October":
            month=10
        if month_name == "November":
            month=11
        if month_name == "December":
            month=12
        #get all file fields
        chronicle_data=Chronicle.objects.filter(date_from__year=year,date_from__month=month)
        context['chronicles']=chronicle_data
        context['chronicle_count']=len(chronicle_data)
        return ''

@register.tag
def do_archive2016(parser, token):
    # token is the string extracted from the template, e.g. "do_foo my_object"
    # it will be splitted, and the second argument will be passed to a new
    # constructed FooNode
    try:
        tag_name, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return FooNode(obj)
