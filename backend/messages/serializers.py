from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatUserSerializer(serializers.ModelSerializer):
      class Meta:
            model = User
            fields = ['id', 'email']

class MessageSerializer(serializers.ModelSerializer):
      sender = serializers.PrimaryKeyRelatedField(read_only=True)
      receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

      class Meta:
            model = Message
            fields = ['id', 'sender', 'receiver', 'message_text', 'timestamp']

      def create(self, validated_data):
            validated_data.pop('sender',None)
            return Message.objects.create(sender=self.context['request'].user,**validated_data)
