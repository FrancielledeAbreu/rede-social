
from rest_framework.routers import DefaultRouter
from likes.views import LikeIdView


router = DefaultRouter()
router.register(r'timeline/post', LikeIdView)
urlpatterns = router.urls
