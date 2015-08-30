class UserTypes(object):
    INTERN = 1
    ORG = 2
    CHOICES = ((INTERN, 'Intern'), (ORG, 'Organization'))

class SubmissionStatus(object):
    REGISTERED = 1
    SUBMITTED = 2
    REJECTED = 3
    ACCEPTED = 4
    CHOICES = (
        (REGISTERED, 'Registered'),
        (SUBMITTED, 'Submitted'),
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted')
    )
