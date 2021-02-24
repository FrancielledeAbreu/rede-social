from django.urls import path
from .views import PostView, CommentView, CommentIdView, LikeIdView

urlpatterns = [
    path('timeline/', PostView.as_view()),
    path('timeline/comments/', CommentView.as_view()),
    path('timeline/comments/<int:id>/', CommentIdView.as_view()),
    path('timeline/post/<int:id>/', LikeIdView.as_view()),
]
