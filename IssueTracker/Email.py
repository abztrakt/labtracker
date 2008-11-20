import LabtrackerCore.Email as Email

class NewIssueEmail(Email.Email):

    def __init__(self, instance):
        subject= instance.title

        # fill out the sections here
        sections = []

        Email.Email.__init__(self, subject=subject,
                sections=sections)

