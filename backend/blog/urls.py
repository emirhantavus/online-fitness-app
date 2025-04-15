from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()

router.register(r'api/posts', PostViewSet)
router.register(r'api/comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]