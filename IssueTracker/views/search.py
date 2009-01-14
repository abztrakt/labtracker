from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import RequestContext

from django.db.models import ObjectDoesNotExist

import IssueTracker.models as im
import IssueTracker.search as issueSearch
import IssueTracker.utils as utils

@permission_required('IssueTracker.can_view', login_url="/login/")
def search(request, page=1):
    """
    Takes a post, searches, and either redirects to a list of matching items (or no
    items), or the specific issue
    """
    extra_context = {}

    data = request.REQUEST.copy()

    if data:
        # in this case, we get to process the stuff
        term = data.get('search_term', False)

        if term:
            try:
                issue_id = int(term)

                # if this is an issue id, then send them to that view
                issue = im.Issue.objects.get(pk=issue_id)
                return HttpResponseRedirect(reverse('IssueTracker-view', args=[issue_id]))
            except ObjectDoesNotExist, e:
                # search_term was not an id, search by string
                pass
            except ValueError, e:
                # search_term was not an id, search by string
                pass

            issues = issueSearch.titleSearch(term)
            args =  utils.generatePageList(request, issues, page)

            args['last_search_term'] = term

            #extra_context['error'] = 'Issue with id "%i" not found.' % term
        else:
            args = utils.generatePageList(request, Issue.objects.all(), page)

        return render_to_response("issue_list.html", args,
                context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect("/")

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

