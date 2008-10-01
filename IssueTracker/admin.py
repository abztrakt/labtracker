from django.contrib import admin
from django.db import models

from IssueTracker import models as itmod

admin.site.register(itmod.ResolveState)
admin.site.register(itmod.ProblemType)

