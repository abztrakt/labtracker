import LabtrackerCore as core

def getInventoryType(name):
    namespace = name.split('.')[-2]
    it = core.models.InventoryType.objects.get(namespace=namespace)
    return it
