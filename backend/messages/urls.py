from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, UserListView

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('chat-users/', UserListView.as_view(), name='chat-user-list'),
]

urlpatterns += router.urls
