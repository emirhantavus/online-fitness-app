from rest_framework import serializers
from .models import (User, UserProfile)
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

class UserProfileSerializer(serializers.ModelSerializer):
      profile_pic = serializers.ImageField(required=False)
      first_name = serializers.CharField(source='user.first_name', required=False)
      last_name = serializers.CharField(source='user.last_name', required=False)
      email = serializers.EmailField(source='user.email', read_only=True)     
      
      class Meta:
            model = UserProfile
            fields = ['id','bio', 'location', 'profile_pic', 'first_name', 'last_name', 'email'] 
          
      def update(self, instance, validated_data):
            user_data = validated_data.pop('user', {})
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')      
            instance.bio = validated_data.get('bio', instance.bio)
            instance.location = validated_data.get('location', instance.location)  

            if first_name:
                    instance.user.first_name = first_name
            if last_name:
                    instance.user.last_name = last_name     
            instance.save()
            instance.user.save()
            return instance
    
class UserSerializer(serializers.ModelSerializer):
      userprofile = UserProfileSerializer(required=False)   
      
      class Meta:
            model = User
            fields = ['id','email', 'first_name', 'last_name', 'password', 'userprofile']
            extra_kwargs = {'password': {'write_only': True}} 
            
      def create(self, validated_data):
            user_profile_data = validated_data.pop('userprofile', None)
            password = validated_data.pop('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            
            if user_profile_data:
                UserProfile.objects.create(user=user, **user_profile_data)
            return user
      
      
class PasswordResetSerializer(serializers.Serializer):
      email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
      new_password = serializers.CharField(write_only=True)
      uidb64 = serializers.CharField()
      token = serializers.CharField()     
      def validate(self, data):
            try:
                  uid = urlsafe_base64_decode(data['uidb64']).decode()
                  user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                  raise serializers.ValidationError("Invalid UID or Token") 
            
            if not default_token_generator.check_token(user, data['token']):
                  raise serializers.ValidationError("Invalid token")  
            
            user.set_password(data['new_password'])
            user.save()
            return data

class UserProfileSerializerTwo(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'profile_pic']

class PasswordChangeSerializer(serializers.Serializer):
      old_password = serializers.CharField(write_only=True)
      new_password = serializers.CharField(write_only=True)
       
      def validate_old_password(self, value):
            user = self.context['request'].user
            if not user.check_password(value):
                  raise serializers.ValidationError("Old password is not correct")
            return value  
      
      def save(self):
            user = self.context['request'].user
            user.set_password(self.validated_data['new_password'])
            user.save()
            
            
            
class TrainerSerializer(serializers.ModelSerializer):
      userprofile = UserProfileSerializerTwo()
      class Meta:
            model = User
            fields = ('id', 'email', 'first_name', 'last_name', 'monthly_rate','userprofile')
        
      def update(self, instance, validated_data):
            userprofile_data = validated_data.pop('userprofile', None)

            # Update User instance
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.monthly_rate = validated_data.get('monthly_rate', instance.monthly_rate)
            instance.save()

            # Update UserProfile instance
            if userprofile_data:
                  UserProfile.objects.update_or_create(user=instance, defaults=userprofile_data)

            return instance
        
class StudentSerializer(serializers.ModelSerializer):
      userprofile = UserProfileSerializer()
      class Meta:
            model = User
            fields = ('id', 'email', 'first_name', 'last_name','userprofile')