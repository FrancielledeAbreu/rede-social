from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AccountView, LoginView, UserView,   UserNameView

urlpatterns = [
    path('accounts/', AccountView.as_view()),
    path('login/', LoginView.as_view()),
]

router = DefaultRouter()
router.register(r'members', UserView)
router.register(r'members/search', UserNameView)
urlpatterns += router.urls
