from django.urls import path
from .views import NotificationView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'mynotifications', NotificationView)
urlpatterns = router.urls
