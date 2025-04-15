from rest_framework import serializers
from .models import (Banners , ExerciseVideo , VideoInstruction, Contact )

class bannerSerializer(serializers.ModelSerializer):
      class Meta:
            model = Banners
            fields = ('img','alt_text')
            
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseVideo
        fields = ['id', 'title', 'video_url','slug']
            
class VideoInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoInstruction
        fields = ['step_number', 'instruction_text']
        
        
class VideoSerializerDetail(serializers.ModelSerializer):
    instructions = VideoInstructionSerializer(many=True, read_only=True)
    class Meta:
        model = ExerciseVideo
        fields = ['id', 'title', 'video_url','slug','instructions']
        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message', 'created_at']