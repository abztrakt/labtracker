import Viewer.models as vm

def getViewType(name):
    namespace = name.split('.')[-1]
    return vm.ViewType.objects.get(name=namespace)
