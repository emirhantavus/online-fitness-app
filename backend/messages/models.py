from django.db import models
from django.conf import settings

class Message(models.Model):
      sender = models.ForeignKey('users.User', related_name='sent_messages', on_delete=models.CASCADE)
      receiver = models.ForeignKey('users.User', related_name='received_messages', on_delete=models.CASCADE)
      message_text = models.TextField()
      timestamp = models.DateTimeField(auto_now_add=True)

      def __str__(self):
          return f'{self.sender} to {self.receiver}: {self.message_text[:20]}'