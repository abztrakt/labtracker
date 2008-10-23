from django import template
from django.core.urlresolvers import reverse

import re

register = template.Library()

"""
For some reason this code is breaking on iteration through the 
all issues view.  It seems like the variable issue that serves 
as a holder for iteration, doesn't change from the previously 
set machine_string and messes up the next iteration if there is 
no item associated with the issue
"""

class LookupMachineNode(template.Node):
    def __init__(self, machine_string):
        self.machine_string = machine_string

    def render(self, context):

        if type(self.machine_string) == unicode:
            return 'None'
        
        self.machine_string = self.machine_string.resolve(context)
        return "<a href=\"%s\">%s</a>" % (reverse('history', args=[self.machine_string]), self.machine_string)

@register.tag('lookup_machine')
def lookup_machine(parser, token):
    try:
        tag_name, machine_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return LookupMachineNode(parser.compile_filter(machine_string))

class SearchHeader(template.Node):
    def __init__(self, col_name, id):
        self.name = col_name
        self.id = id

    def render(self, context):
        return """
        <th class='r_%s'>
            <a href="?orderby=%s&ometh=%s">%s</a>
        </th>""" % (self.id, self.id.resolve(context), context['omethod'], self.name.resolve(context))

@register.tag('searchcolumn')
def column_header(parser, token):
    try:
        tag_name, id, col_name = token.split_contents()
        id, col_name = map(template.Variable, [id, col_name])
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return SearchHeader(col_name, id)
