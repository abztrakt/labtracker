from django.core.mail import send_mail
from django.conf import settings

class EmailSection(object):
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

class Email(object):

    def __init__(self, subject="", sections=[], to=[], sender=settings.DEFAULT_FROM_EMAIL):
        for section in sections:
            if not isinstance(section, EmailSection):
                raise Exception, "section given was not an emailsection type"

        self.sections = sections
        self.subject = subject
        self.to = to
        self.sender = sender

    def empty(self):
        if not self.sections:
            return True

        for section in self.sections:
            if section.empty():
                return True

        return False


    def appendSection(self, section):
        if not isinstance(section, EmailSection):
            raise Exception, "section given was not an emailsection type"

        self.sections.append(section)

    def addTo(self, to):
        # FIXME validate these emails before adding to list
        self.to.append(to)

    def send(self, auth_user=None, auth_password=None):
        """
        Send the email
        """

        message = "\n\n".join([section.__str__() for section in self.sections])

        send_mail(self.subject, message, self.sender, self.to,
                auth_user=auth_user, 
                auth_password=auth_password)
