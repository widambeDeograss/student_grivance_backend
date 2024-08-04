from django.urls import path
from .views import *

app_name = 'grivance_management'

urlpatterns = [
    path('divisions', DivisionView.as_view()),
    path('sub_divisions', SubDivisionView.as_view()),
    path('problem_type', ProblemTypeView.as_view()),
    path('submit_grivence', SubmittedProblemsView.as_view()),
    path('problem_evdc', ProblemEvidenceView.as_view()),
    path('suggestions', SuggestionsViewSet.as_view()),
    path(
        "suggestions/<uuid:pk>/",
        SuggestionsRetrieveUpdateDestroyAPIView.as_view(),
        name="suggestions",
    ),
    path('notifications', NotificationView.as_view()),
    path('dashboard_stats', DashBoardStats.as_view()),
    path('dit_grievance_workflow', GrievanceWorkFlow.as_view(), name='grievance-workflow'),
]