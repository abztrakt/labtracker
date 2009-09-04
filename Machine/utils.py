import Machine.models as m_models

def updateStatus(machine, status, user, time):
    """
    update the status of a machine
    """

    machine.status = status
    machine.save()

    # TODO will need to implement a way to keep current status of the machine
    # without going to history table

    hist = m_models.History(machine=machine, ms=status, 
            user=user, time=time)
    hist.save()

def get_all_macs():
    """Returns a list of all mac address for machines"""
    macs = []
    machines = m_models.Item.objects.all() 
    
    for machine in machines:
        macs.append(machine.mac1)
        if machine.mac2 is not None or machine.mac2 != '':
            macs.append(machine.mac2)

    return macs
