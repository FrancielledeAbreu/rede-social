from django.urls import path
from .views import LikeIdView

urlpatterns = [
    path('timeline/post/<int:id>/', LikeIdView.as_view())
]
