from django.urls import path
from .views import CommentView, CommentIdView

urlpatterns = [
    path('timeline/comments/', CommentView.as_view()),
    path('timeline/comments/<int:id>/', CommentIdView.as_view())

]
