from django import newforms as forms
class CreateIssueForm(forms.Form):
    """
    Need to know, inventory type
    Group of items (optional)
    item (optional)
    assignee (primary contact default)
    title
    description
    problem_type 
    """
    title = forms.CharField(max_length=60)
    description = forms.TextField()


