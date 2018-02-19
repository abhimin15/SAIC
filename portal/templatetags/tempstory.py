from django import template
from portal.models import *
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
        temp_category=obj.category
        if temp_category == 'alumni':
            temp_user=AluminiDetails.objects.get(email=obj.who_posted)
        elif temp_category == 'student':
            temp_user=StudentDetails.objects.get(email=obj.who_posted)
        elif temp_category == 'faculty':
            temp_user=FacultyDetails.objects.get(email=obj.who_posted)
        context['story_user']=temp_user
        return ''

@register.tag
def do_story(parser, token):
    # token is the string extracted from the template, e.g. "do_foo my_object"
    # it will be splitted, and the second argument will be passed to a new
    # constructed FooNode
    try:
        tag_name, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return FooNode(obj)
