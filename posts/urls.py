from django.urls import path
from .views import PostView, PostPrivateView

urlpatterns = [
    path('timeline/', PostView.as_view()),
    path('timeline/private', PostPrivateView.as_view()),
]
