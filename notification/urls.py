from django.urls import path
from .views import NotificationView

urlpatterns = [
    path('mynotification/', NotificationView.as_view()),

]
