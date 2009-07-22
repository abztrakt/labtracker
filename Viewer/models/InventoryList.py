import os

from django.db import models 
from django.conf import settings

from labtracker.Viewer.models import base
import labtracker.Viewer.utils 
import labtracker.LabtrackerCore.models as c_models
import labtracker.Machine.models as m_models

app_name = __name__.split('.')[-3]

class InventoryList(base.ViewCore):
    view = models.OneToOneField(base.ViewCore, parent_link=True, editable=False)
    
    """
    @models.permalink
    def get_absolute_url(self):
        return ('Viewer-InventoryList-Items', [str(self.shortname)])
    """

    class Meta:
        app_label = "Viewer"
