from django.core.management import setup_environ
import settings

setup_environ(settings)

from labtracker.Machine.models import Item, Location, Group, Type, Platform
from labtracker.LabtrackerCore.models import InventoryType
import re
import sys

# Collect the data and store them into lists containing dictionaries

if not sys.argv[1]:
    print "Argument: file containing machine data to load into LabTracker."
    sys.exit(1)

file = open(sys.argv[1], "r")

if not file:
    print "Error: file could not be opened."
    sys.exit(1)

it = InventoryType.objects.filter(name='Machine')
type = Type.objects.filter(name='Unknown')
platform = Platform.objects.filter(name='Unknown')

if platform.count() < 1:
    platform = Platform(name='Unknown', description='Unknown platform type')
    platform.save()
else:
    platform = platform.get(name='Unknown')

if type.count() < 1:
    type = Type(name='Unknown', platform=platform, model_name='Unknown', specs='Unknown')
    type.save()
else:
    type = type.get(name='Unknown')

if it.count() < 1:
    it = InventoryType(name='Machine', namespace='Machine', description='Computers and Workstations')
    it.save()
else:
    it = it.get(name='Machine')

location = ""
segments = []
item = {}
for line in file.readlines():
    if (line.startswith(";")):
        item['location'] = re.sub("[^a-zA-Z0-9]", "", line[1:])
        # save 
        location = Location.objects.filter(name=item['location'])
        if location.count() < 1:
            location = Location(name=item['location'])
            location.save()
        else:
            location = location.get(name=item['location'])

        m_group = Group.objects.filter(name=item['location'])
        if m_group.count() < 1:
            m_group = Group(name=item['location'], it=it, casting_server='100.0.0.0', gateway='100.0.0.0')
            m_group.save()
        else:
            m_group = m_group.get(name=item['location'])

    elif not re.match("^([ ]|\n|\t)", line):
        # get segments of a line in a given location
        segments = line.split("\t")
        item['name'] = segments[0]
        item['ip'] = segments[1]
        item['cast'] = segments[2]
        item['mac'] = segments[3]
        item['gateway'] = segments[4]
        item['service_tag'] = segments[5]
        
        print "name: %s, location: %s, ip: %s, casting server: %s, mac: %s, gateway: %s, service tag: %s" % (item['name'], item['location'], item['ip'], item['cast'], item['mac'], item['gateway'], item['service_tag'])
        
        # save into models
        # save location into LabtrackerCore.Group, Machine.Group, Machine.Location
        machine = Item.objects.filter(name=item['name'])

        if machine.count() < 1:
            machine = Item(name=item['name'], type=type, it=it, location=location, ip=item['ip'], mac1=item['mac'], wall_port='unknown', manu_tag=item['service_tag'])
        else:
            machine = machine.get(name=item['name'])
            machine.mac = item['mac']
            machine.manu_tag = item['service_tag']
            machine.ip = item['ip']

        machine.save()
        
        m_group.items.add(machine)
        m_group.save()
