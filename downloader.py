from django.core.management import setup_environ
import settings

setup_environ(settings)

from labtracker.Machine.models import Item, Location, Group, Type, Platform
from labtracker.LabtrackerCore.models import InventoryType
import re
import sys

# Write all machine item data into a text file

# Collect information from Machine.models.Items and link to parent
if not sys.argv[1]:
    print "Argument: filename of which to write machine data."
    sys.exit(1)

output = open(sys.argv[1], "w")

for location in Location.objects.all():
    group = Group.objects.filter(name=location.name)[0]

    line = "; %s" % (group.name)

    line = line + " ===================================             \n"
    output.write(line)

    for machine in Item.objects.filter(location=location):
        line = "%s\t%s\t%s\t%s\t%s\t%s" % (machine.name, machine.ip, group.casting_server, machine.mac1, group.gateway, machine.manu_tag)
        output.write(line)
    output.write("\n")
