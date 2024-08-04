from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Division)
admin.site.register(SubDivision)
admin.site.register(ProblemType)
admin.site.register(SubmittedProblems)
admin.site.register(TrackProblem)
admin.site.register(ProblemEvidence)
admin.site.register(Notification)
admin.site.register(Suggestions)