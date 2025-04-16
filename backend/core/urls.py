from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BannersList,
    VideoViewSet,
    VideoDetailViewSet,
    ContactView,
    NutritionAPIView
)

router = DefaultRouter()
router.register(r"banners", BannersList, basename="banners")
router.register(r"videos", VideoViewSet, basename="videos")

urlpatterns = [
      path("", include(router.urls)),
      path("videos/<slug:slug>/detail/", VideoDetailViewSet.as_view(), name="video-detail"),
      path("contact/", ContactView.as_view(), name="contact"),
      path('nutrition/', NutritionAPIView.as_view(),name='nutrition-api'),
]