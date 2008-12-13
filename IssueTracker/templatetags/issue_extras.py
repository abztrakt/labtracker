from django import template
from django.core.urlresolvers import reverse

from IssueTracker import utils

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
    #XXX not used
    def __init__(self, machine_string):
        self.machine_string = machine_string

    def render(self, context):
        if type(self.machine_string) == unicode:
            return 'None'
        
        self.machine_string = self.machine_string.resolve(context)
        return "<a href=\"%s\">%s</a>" % (reverse('history', args=[self.machine_string]), self.machine_string)

@register.tag('lookup_machine')
def lookup_machine(parser, token):
    #XXX not used
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
        id = self.id.resolve(context)
        name = self.name.resolve(context)

        row = '<th class="r_%s">%%s</th>' % (id)
        text = name
        link = '<a href="?orderby=%s&ometh=%s">%%s</a>' % \
                    (id, context['omethod'])

        if context['orderby'] == id:
            if context['omethod'] == 'ASC':
                image = 'desc.png'
            else:
                image = 'asc.png'
            img = '<img src="/static/img/layout/%s" />' % (image)
            text = img + text

        return row % (link % text)


@register.tag('searchcolumn')
def column_header(parser, token):
    try:
        tag_name, id, col_name = token.split_contents()
        id, col_name = map(template.Variable, [id, col_name])
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments" % token.contents.split()[0]
    return SearchHeader(col_name, id)

class PrimaryContact(template.Node):
    def __init__(self, issue):
        self.issue = template.Variable(issue)

    def render(self, context):
        issue = self.issue.resolve(context)

        if issue == None:
            return

        contacts = utils.getIssueContacts(issue)
        
        if contacts == None or len(contacts) < 1:
            return

        # get the contact names
        names = [u.username for u in contacts]

        return ", ".join(names)


@register.tag('contact')
def primary_contact(parser, token):
    """
    Give the primary contacts for issue
    """
    try:
        tag_name, issue = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return PrimaryContact(issue)

class InventorySpecific(template.Node):
    def __init__(self, issue):
        self.issue = template.Variable(issue)

    def render(self, context):
        issue = self.issue.resolve(context)
        inv_t = issue.it

        # call the hook if it exists
        hook = utils.issueHooks.getViewHook(inv_t.name)

        if hook == None:
            return ""

        return hook(context, issue)

@register.tag('invspec')
def invSpec(parser, token):
    try:
        tag_name, issue = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
                "%r tag requires a single argument" % token.contents.split()[0]
    return InventorySpecific(issue)


class InventorySpecificUpdate(template.Node):
    def __init__(self, issue):
        self.issue = template.Variable(issue)

    def render(self, context):
        issue = self.issue.resolve(context)
        inv_t = issue.it

        # call the hook if it exists
        hook = utils.issueHooks.getUpdateHook(inv_t.name)

        if hook == None:
            return ""

        return hook(context, issue)

@register.tag('invspecUpdate')
def invSpecUpdate(parser, token):
    try:
        tag_name, issue = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
                "%r tag requires a single argument" % token.contents.split()[0]
    return InventorySpecificUpdate(issue)

@register.inclusion_tag('issue/list_block.html', takes_context=True)
def issueList(context, list, grouper=None):
    return { 'object_list': list, 
            'grouper': grouper,
            'omethod': context['omethod'],
            'orderby': context['orderby'] }
