from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostView, PostPrivateView, FeedView

urlpatterns = [
    path('timeline/private', PostPrivateView.as_view()),
    path('feed/', FeedView.as_view()),
]


router = DefaultRouter()
router.register(r'timeline', PostView)
urlpatterns += router.urls
