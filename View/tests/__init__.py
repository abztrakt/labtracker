from django.test import TestCase
import LabtrackerCore.models as c_models
import Machine.models as m_models
import View.models as v_models

from View.tests.MachineMap import *

class ViewTest(TestCase):
    fixtures = ['test',]
