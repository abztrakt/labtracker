from django.forms import ValidationError
#from django.core.validators import email_re
from django.core import mail 
#from django.core import validators
from django.conf import settings
from django.template.loader import render_to_string

try:
    from django.core.validators import email_re
except ImportError:
    from django.forms.fields import email_re


class EmailSection(object):
    """
    A section in the body of an email

    Section is composed of a header followed by content
    """

    def __init__(self, header = "", content = ""):
        self.header = header
        self.content = content

    def empty(self):
        """
        Returns true if header and content are both empty
        """
        return not(self.header or self.content)

    def __str__(self):
        if not self.content:
            return "%s\n" % self.header

        return "%s:\n%s" % (self.header, self.content)

def isValidEmail(email):
    """
    returns true if email is valid, false if not
    """
    return email not in (u'', '') and email_re.search(email)

class Email(object):
    """
    Email object itself, should be composed of many sections
    """
    def __init__(self, subject="", sections=[], to=[], cc=[], bcc=[], 
            sender=settings.DEFAULT_FROM_EMAIL):
        for section in sections:
            if not isinstance(section, EmailSection):
                raise Exception, "section given was not an emailsection type"

        if type(sections) != list:
            self.sections = [sections]
        else:
            self.sections = sections

        self.subject = subject

        # check email valid
        emails = set(to)
        emails.update(cc)
        emails.update(bcc)
        for em in emails:
            if not isValidEmail(em):
                raise ValidationError("Invalid Email")

        self.to = set(to)               # uniquify
        self.cc = set(cc)
        self.bcc = set(bcc)
        self.sender = sender

    def empty(self):
        """
        Test and see if the email has sections and is not empty
        """

        if not self.sections:
            return True

        for section in self.sections:
            if section.empty():
                return True

        return False

    def appendSection(self, section):
        """
        Create new section
        """

        if not isinstance(section, EmailSection):
            raise Exception, "section given was not an emailsection type"

        self.sections.append(section)

    def addCC(self, to):
        """
        Add a 'to' address
        """
        if isValidEmail(to):
            self.cc.add(to)

    def addBCC(self, to):
        """
        Add a 'to' address
        """
        if isValidEmail(to):
            self.bcc.add(to)

    def addTo(self, to):
        """
        Add a 'to' address
        """
        if isValidEmail(to):
            self.to.add(to)

    def getEmail(self, auth_user=None, auth_password=None):
        #message = "\n\n".join([section.__str__() for section in self.sections])
        header_message = ""
        message = header_message + render_to_string('email/email_message.txt', {"all_sections": self.sections })

        to = self.to.union(self.cc)

        connection = mail.SMTPConnection(username=auth_user, password=auth_password,
                fail_silently=False)
        email = mail.EmailMessage(self.subject, message, self.sender, 
                to, bcc=self.bcc, connection=connection)
        return email

    def send(self, auth_user=None, auth_password=None):
        """
        Send the email
        """
        email = self.getEmail()
        if email.to == '':
            return email.send(fail_silently=True)
        return email.send()

"""
class NewIssueEmail(Email):
    def __init__(self, issue, *args, **kwargs):
        Email.__init__(self, *args, **kwargs)

        self.appendSection(EmailSection(
            "New Issue:",
            "Issue: %s\nTitle: %s" % (issue.pk, issue.title)
        ))

        for cc in issue.cc.all():
            self.addCC(cc.email)
"""

