from django.urls import path
from .views import AccountView, LoginView, UserView, UserIdView

urlpatterns = [
    path('accounts/', AccountView.as_view()),
    path('login/', LoginView.as_view()),
    path('members/', UserView.as_view()),
    path('members/<int:id>/', UserIdView.as_view())

]
