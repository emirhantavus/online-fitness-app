from django.shortcuts import render
from .serializers import (UserProfileSerializer, UserSerializer,
                          PasswordResetConfirmSerializer, PasswordChangeSerializer , PasswordResetSerializer,
                          TrainerSerializer, StudentSerializer)
from .models import (User, UserProfile)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate , login ,logout
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.dateformat import format
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from messages.serializers import ChatUserSerializer
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsTrainer
from programs.models import TrainerStudentProgram

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
class SpecificUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user_profile = get_object_or_404(UserProfile, user__id=user_id)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    
    def patch(self, request, user_id):
        try:
            if request.user.id != int(user_id):
                return Response({"error":"U do not have permission to edit this profile."},status=status.HTTP_403_FORBIDDEN)
            
            user_profile = get_object_or_404(UserProfile, user__id=user_id)
            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
      
      
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = user.tokens()
            return Response(tokens, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_trainer:
                return Response({'error':'Trainers are not allowed to login from this page.'}, status=status.HTTP_403_FORBIDDEN)
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Successful login',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_trainer':user.is_trainer,
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name})
        else:
            return Response({'error': 'Wrong email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class TrainerLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if not user.is_trainer:
                return Response({'error': 'Only trainers are allowed to login from this page.'}, status=status.HTTP_403_FORBIDDEN)
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Successful login',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_trainer':user.is_trainer,
                'user_id':user.id,
                'first_name': user.first_name,
                'last_name':user.last_name})
        else:
            return Response({'error': 'Wrong email or password'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout success'}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({'error': "'refresh' token not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class MyTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)
    
    
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"{request.scheme}://{request.get_host()}/api/password-reset-confirm/{uid}/{token}/"

                send_mail(
                    'Password Reset Request',
                    f'Click the link below to reset your password:\n{reset_link}',
                    'no-reply@myapp.com',
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data={
            'new_password': request.data.get('new_password'),
            'uidb64': uidb64,
            'token': token,
        })
        if serializer.is_valid():
            return Response({"message": "Password has been reset."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been changed."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ChatUserSerializer
    permission_classes = [IsAuthenticated]
    
    
class TrainerViewSet(ModelViewSet):
    queryset = User.objects.filter(is_trainer=True)
    serializer_class = TrainerSerializer
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsTrainer]
    
    def get_queryset(self):
        trainer = self.request.user
        if not trainer.is_trainer:
            return User.objects.none()
        student_ids = TrainerStudentProgram.objects.filter(trainer=trainer).values_list('student_id', flat=True)
        return User.objects.filter(id__in=student_ids, is_trainer=False).distinct()