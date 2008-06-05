import View.models as vm

def getViewType(name):
    namespace = name.split('.')[-1]
    print namespace
    return vm.ViewType.objects.get(name=namespace)
