from django.core.management import setup_environ
import settings

setup_environ(settings)

from labtracker.Machine.models import Item, Location, Group, Type, Platform
from labtracker.LabtrackerCore.models import InventoryType
import re
import sys

# Collect the data and store them into lists containing dictionaries
FORCE_DELETE = False

def status(item, status):
    print "\nname: %s, location: %s, ip: %s, casting server: %s, mac: %s, gateway: %s, service tag: %s%s" % (item['name'], item['location'], item['ip'], item['cast'], item['mac'], item['gateway'], item['service_tag'], status)

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
    if re.match("^[a-zA-Z]", line): # row to input into database
        segments = line.split("\t")
        item['name'] = segments[0]
        item['ip'] = segments[1]
        item['cast'] = segments[2]
        # MAC address is not in standard aa:bb:cc:dd:ee:ff format
        if re.match("^[a-zA-Z0-9]{12}$", segments[3]):
            item['mac'] = segments[3][0:2]
            for i in range(1, len(segments[3]) / 2):
                item['mac'] += ":" + segments[3][2*i:2*i+2]
        else:
            item['mac'] = "00:00:00:00:00:00"

        item['gateway'] = segments[4]
        item['service_tag'] = ""
        if len(segments) > 6:
            item['service_tag'] = segments[6]
        
        item['location'] = re.findall("^[a-zA-Z0-9]*", segments[0])[0] # currently the only way to truly determine location. may be problematic with access+ locations.
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
        
        m_group.casting_server = item['cast']
        m_group.gateway = item['gateway']
 

        # save into models
        # save location into LabtrackerCore.Group, Machine.Group, Machine.Location
        machine = Item.objects.filter(name=item['name'])
        invalid = False
        # if machine name doesn't exist, check if MAC exists
        if machine.count() < 1:
            machine = Item.objects.filter(mac1=item['mac'])
            if (machine.count() == 1) and (item['mac'] == machine[0].mac1) and not (item['mac'] == "00:00:00:00:00:00"): # if MAC exists and matches, overwrite
                machine = machine.get(mac1=item['mac'])
                machine.mac = item['mac']
                machine.name = item['name']
                machine.manu_tag = item['service_tag']
                machine.ip = item['ip']
                status(item, "MAC exists, name doesn't exist, overwrite")
            else: # MAC doesn't exist or match, then add new machine
                machine = Item(name=item['name'], type=type, it=it, location=location, ip=item['ip'], mac1=item['mac'], wall_port='unknown', manu_tag=item['service_tag'])
#                status(item, "MAC doesn't exist, name doesn't exist, add new")
        else: # else name does exist, check if MAC exists
            if item['mac'] == machine[0].mac1: # if MACs match, then overwrite
                machine = machine.get(name=item['name'])
                machine.mac = item['mac']
                machine.manu_tag = item['service_tag']
                machine.ip = item['ip']
                status(item, "MAC exists, name exists, overwrite")
            else: # else MACs are different, do not load and return error message
                machine = machine[0]
                if machine.manu_tag == item['service_tag'] and not machine.mac2 and not machine.mac1 == item['service_tag']:
                    print "Adding second MAC address %s to %s" % (item['mac'], item['name'])
                    machine.mac2 = item['mac']
                elif FORCE_DELETE: # overwrite old machine with new data
                    print "Force overwriting %s, new MAC: %s, overwritten MAC: %s" % (item['name'], item['mac'], machine.mac1)
                    machine.mac1 = item['mac']
                    machine.manu_tag = item['service_tag']
                    machine.ip = item['ip']
                else:
                    invalid = True
                    print "Error writing %s with MAC address %s. Duplicate entry containing same machine name and different MAC address. Existing MAC address in database: %s" % (item['name'], item['mac'], machine.mac1)

        if not invalid or FORCE_DELETE:
            machine.save()
            m_group.items.add(machine)
            m_group.save()
            print "Successfully saved %s, %s" % (machine.name, machine.mac1)

