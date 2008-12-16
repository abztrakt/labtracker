from django.core import mail 
#from django.core import validators
from django.conf import settings

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
    returns true if email is valid
    """
    # FIXME fix validtaor
    #validators.isValidEmail(email, None)
    return True

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
            isValidEmail(em)            # raises ValidationError

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
        Add a section to the email
        """

        if not isinstance(section, EmailSection):
            raise Exception, "section given was not an emailsection type"

        self.sections.append(section)

    def addCC(self, to):
        """
        Add a 'to' address
        """
        isValidEmail(to)            #raises ValidationError
        self.cc.add(to)

    def addBCC(self, to):
        """
        Add a 'to' address
        """
        isValidEmail(to)            #raises ValidationError
        self.bcc.add(to)

    def addTo(self, to):
        """
        Add a 'to' address
        """
        isValidEmail(to)            #raises ValidationError
        self.to.add(to)

    def getEmail(self, auth_user=None, auth_password=None):
        message = "\n\n".join([section.__str__() for section in self.sections])

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

