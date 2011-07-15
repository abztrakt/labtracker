import LabtrackerCore as core
from django.core.paginator import Paginator, EmptyPage, InvalidPage 

def getInventoryType(name):
    namespace = name.split('.')[-2]
    it = core.models.InventoryType.objects.get(namespace=namespace)
    return it

def generateOrderingArgs(request, qdict):
    """
    Create issue args for rendering a view issue form
    """
    data = request.GET.copy()

    orderby = data.get('orderby', 'pk')
    omethod = data.get('ometh', 'ASC')
    order_symbol = ('-', '')[omethod == 'ASC']

    objects = qdict.order_by(order_symbol + orderby)

    args = {
        'orderby':  orderby,
        'objects': objects,
        'omethod':  ('ASC', 'DESC')[omethod=='ASC'],
        'search_term':  data.get('search_term')
    }

    return args

def generatePageList(request, qdict, page_num):
    """
    Generates args needed for issue_list template
    Take some arguments from user in data, the page number to show and the 
    returned query items, render out to user
    """
    #Doesn't even get used???
    #data = request.GET.copy()

    # TODO need user-defined limits
    # num_per_page = 100

    args = generateOrderingArgs(request, qdict)

    #ALL of the objects (issues)
    objects = args['objects']
    
    #Paginate ALL of the objects (issues in this case)
    p = Paginator(objects, 30)

    #Attempt to grab a page number, if not available, go to first page
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        args['page'] = p.page(page)
    except (EmptyPage, InvalidPage):
        args['page'] = p.page(p.num_pages)

    if args['search_term']:
        # kludgy way of doing things
        args['extraArgs'] = '&search_term=%s' % ( args['search_term'] )

    return args


