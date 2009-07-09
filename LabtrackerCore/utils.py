import LabtrackerCore as core
from django.core.paginator import Paginator 

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

    data = request.GET.copy()

    # TODO need user-defined limits
    num_per_page = 100

    args = generateOrderingArgs(request, qdict)

    objects = args['objects']

    p = Paginator(objects, 30)

    args['page'] = p.page(page_num)

    if args['search_term']:
        # kludgy way of doing things
        args['extraArgs'] = '&search_term=%s' % ( args['search_term'] )

    return args


