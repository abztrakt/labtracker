from django.core import validators
from django.core.mail import send_mail, EmailMessage, SMTPConnection
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
    validators.isValidEmail(email, None)

class Email(object):
    """
    Email object itself, should be composed of many sections
    """
    def __init__(self, subject="", sections=[], to=[], cc=[], bcc=[], 
            sender=settings.DEFAULT_FROM_EMAIL):
        for section in sections:
            if not isinstance(section, EmailSection):
                raise Exception, "section given was not an emailsection type"

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

    def send(self, auth_user=None, auth_password=None):
        """
        Send the email
        """


        # TODO send emails to BCC and CC as well

        message = "\n\n".join([section.__str__() for section in self.sections])

        email = EmailMessage(self.subject, message, from_email=self.sender, 
                to=self.to, bcc=self.bcc, 
                connection=SMTPConnection(username=auth_user, password=auth_password))

        email.send()

