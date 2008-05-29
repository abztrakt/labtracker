from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from IssueTracker.models import *
import IssueTracker.search as issueSearch
import IssueTracker.utils as utils

@permission_required('IssueTracker.can_view', login_url="/login/")
def search(request):
    """
    Takes a post, searches, and either redirects to a list of matching items (or no
    items), or the specific issue
    """
    extra_context = {}

    if request.method == "POST":
        data = request.POST
    elif request.method == "GET":
        data = request.GET

    if data:
        # in this case, we get to process the stuff
        issue_id = data.get('search_term', False)

        if issue_id:
            try:
                issue_id = int(issue_id)

                issue = Issue.objects.get(pk=issue_id)
                return HttpResponseRedirect(reverse('view', args=[issue.issue_id]))
            except ValueError, e:
                # search_term was not an id, search by string
                issues = Issue.objects.filter(title__icontains=issue_id)

                return utils.generateList(data, issues, 1)

            except ObjectDoesNotExist, e:
                # issue id was not an actual issue, use it as a search_term
                issues = Issue.objects.filter(title__contains=issue_id)

                # FIXME change so that it uses the generateList as well
                return utils.generateList(data,
                        Issue.objects.all(), 1)

            except Exception, e:
                return HttpResponseServerError()

            #extra_context['error'] = 'Issue with id "%i" not found.' % issue_id
        else:
            return utils.generateList(request, data, Issue.objects.all(), 1)


    else:
        return HttpResponseRedirect(reverse('index'))

@permission_required('IssueTracker.can_view', login_url="/login/")
def advSearch(request):
    """ advSearch

    Takes user to the advanced search form page
    """

    """
    form = SearchForm()
    form.fields['resolved_state'].choices = [
            (state.pk, state.name) for state in ResolveState.objects.all()]
    form.fields['problem_type'].choices = [
            (type.pk, type.name) for type in ProblemType.objects.all()]
    form.fields['inventory_type'].choices = [
            (type.pk, type.name) for type in LabtrackerCore.InventoryType.objects.all()]

    args['form'] = form
    """
    if request.method == 'POST':
        data = request.POST.copy()
        if data['action'] == 'Search':
            # send the data to the search handler
            del(data['action'])
            del(data['fields'])
            searches = issueSearch.parseSearch(data)
            query = issueSearch.buildQuery(searches)

            extra_context = {}

            return HttpResponse(object_list(request, queryset=query, 
                extra_context = extra_context, allow_empty=True))


    args['add_query'] = AddSearchForm()

    return render_to_response('IssueTracker/adv_search.html', args,
            context_instance=RequestContext(request))

