from django.urls import path
from .views import PostView, CommentView, CommentIdView

urlpatterns = [
    path('timeline/', PostView.as_view()),
    path('timeline/comments/', CommentView.as_view()),
    path('timeline/comments/<int:id>/', CommentIdView.as_view()),
]
