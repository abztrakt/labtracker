import Machine.models as m_models

def updateStatus(machine, status, user, time):
    """
    update the status of a machine
    """

    machine.ms = status
    machine.save()

    # TODO will need to implement a way to keep current status of the machine without
    # going to history table

    hist = m_models.History(machine=machine, ms=status, 
            user=user, time=time)
    hist.save()
