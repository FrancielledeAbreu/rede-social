from django.urls import path
from reports.views import ReportViewFollowers, ReportViewFollowing, ReportViewNotification


urlpatterns = [
    path('reports/followers/<int:user_id>/',
         ReportViewFollowers.as_view()),
    path('reports/following/<int:user_id>/',
         ReportViewFollowing.as_view()),
    path('reports/notification/<int:user_id>/',
         ReportViewNotification.as_view())
]
