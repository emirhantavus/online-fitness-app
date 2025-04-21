from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Message
from .serializers import ChatUserSerializer, MessageSerializer


User = get_user_model()

class UserListView(generics.ListAPIView):
      queryset = User.objects.all()
      serializer_class = ChatUserSerializer
      permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(ModelViewSet):
      serializer_class = MessageSerializer
      permission_classes = [permissions.IsAuthenticated]
      pagination_class = None

      def get_queryset(self):
            user = self.request.user
            other_user_id = self.request.query_params.get('user')
            return Message.objects.filter(
                  (Q(sender=user) & Q(receiver_id=other_user_id)) |
                  (Q(sender_id=other_user_id) & Q(receiver=user))
                  ).order_by('timestamp')

      def perform_create(self, serializer):
            serializer.save(sender=self.request.user)