from django.shortcuts import render
from .serializers import (ExerciseListSerializer,ExerciseSerializer, EvolutionSerializer, 
                          TrainerStudentProgramSerializer)

from .models import (Exercise , Evolution, 
                     TrainerStudentProgram)

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework import status , generics
from django.db.utils import IntegrityError
from datetime import datetime , timedelta , timezone
from django.contrib.auth import get_user_model
from core.permissions import IsTrainer , IsStudentOrTrainer


User = get_user_model()

class ExerciseProgramViewSet(ModelViewSet):
      queryset = Exercise.objects.all()
      serializer_class = ExerciseSerializer
      permission_classes = [IsAuthenticated, IsTrainer]

      def create(self, request, *args, **kwargs):
            data = request.data
            program_id = data.get("program_id")

            if not program_id:
                  return Response({'error': 'Program ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                  program = TrainerStudentProgram.objects.get(id=program_id, trainer=request.user)

                  exercise = Exercise.objects.create(
                  program=program,
                  title=data["title"],
                  sets_reps=data["sets_reps"],
                  intensity=data["intensity"],
                  tempo=data.get("tempo", ""),
                  rest=data["rest"],
                  video_url=data["video_url"],
                  day=data["day"]
                  )
                  for week in range(1, 5):
                        Evolution.objects.create(
                              exercise=exercise,
                              week_number=week,
                              description=""
                        )

                  return Response(ExerciseSerializer(exercise).data, status=status.HTTP_201_CREATED)
        
            except TrainerStudentProgram.DoesNotExist:
                  return Response({'error': 'Program not found or you do not have permission to add exercises to this program.'}, status=status.HTTP_400_BAD_REQUEST)

      def get_permissions(self):
            if self.action in ['create', 'update', 'partial_update', 'destroy']:
                  self.permission_classes = [IsAuthenticated, IsTrainer]
            else:
                  self.permission_classes = [IsAuthenticated, IsStudentOrTrainer]
            return super().get_permissions()
    
    
    

class EvolutionViewSet(ModelViewSet):
      queryset = Evolution.objects.all()
      serializer_class = EvolutionSerializer
      permission_classes = [IsAuthenticated, IsStudentOrTrainer]

      def get_queryset(self):
            user = self.request.user
            if user.is_trainer:
                  return Evolution.objects.filter(exercise__program__trainer=user)
            elif user.is_student:
                  return Evolution.objects.filter(exercise__program__student=user)
            return Evolution.objects.none()

      def create(self, request, *args, **kwargs):
            data = request.data
            try:
                  log = Evolution.objects.create(
                        exercise_id=data["exercise_id"],
                        week_number=data["week_number"],
                        description=data["description"]
                        )
                  log.save()
                  return Response(EvolutionSerializer(log).data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                  return Response({'error': 'Invalid exercise_id: Exercise not found or other integrity error.'}, status=status.HTTP_400_BAD_REQUEST)

      def update(self, request, *args, **kwargs):
            instance = self.get_object()
            if request.user != instance.exercise.program.student and request.user != instance.exercise.program.trainer:
                  return Response({'error': 'You do not have permission to update this log'}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      def partial_update(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)

      def list(self, request, *args, **kwargs):
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    
    
class TrainerStudentProgramViewSet(ModelViewSet):
      queryset = TrainerStudentProgram.objects.all()
      serializer_class = TrainerStudentProgramSerializer
      permission_classes = [IsAuthenticated, IsTrainer]

      def get_queryset(self):
            user = self.request.user
            if user.is_staff:
                  return TrainerStudentProgram.objects.all()
            elif user.is_trainer:
                  return TrainerStudentProgram.objects.filter(trainer=user)
            else:
                  return TrainerStudentProgram.objects.filter(student=user)

      def get_permissions(self):
            if self.action in ['create', 'update', 'partial_update', 'destroy']:
                  self.permission_classes = [IsAuthenticated, IsTrainer]
            else:
                  self.permission_classes = [IsAuthenticated, IsStudentOrTrainer]
            return super().get_permissions()

      def create(self, request, *args, **kwargs):
            data = request.data
            student_id = data.get("student_id")
            title = data.get("title")

            if not student_id or not title:
                  return Response({'error': 'Student ID and title are required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                  student = User.objects.get(id=student_id)
                  program = TrainerStudentProgram.objects.create(
                      trainer=request.user,
                      student=student,
                      title=title,
                      start_date=timezone.now(),
                      end_date=timezone.now() + timedelta(days=30)
                  )

                  for exercise_data in data["exercises"]:
                        exercise = Exercise.objects.create(
                            program=program,
                            title=exercise_data["title"],
                            sets_reps=exercise_data["sets_reps"],
                            intensity=exercise_data["intensity"],
                            tempo=exercise_data.get("tempo", ""),
                            rest=exercise_data["rest"],
                            video_url=exercise_data["video_url"],
                            day=exercise_data["day"]
                        )
                        for week in range(1, 5):
                              Evolution.objects.create(
                                    exercise=exercise,
                                    week_number=week,
                                    description=""
                              )

                  return Response(TrainerStudentProgramSerializer(program).data, status=status.HTTP_201_CREATED)
        
            except User.DoesNotExist:
                  return Response({'error': 'Student not found.'}, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as e:
                  return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

      def update(self, request, *args, **kwargs):
            instance = self.get_object()
            data = request.data

            exercises_data = data.get('exercises', [])

            instance.exercises.all().delete()

            for exercise_data in exercises_data:
                  exercise = Exercise.objects.create(
                      program=instance,
                      title=exercise_data["title"],
                      sets_reps=exercise_data["sets_reps"],
                      intensity=exercise_data["intensity"],
                      tempo=exercise_data.get("tempo", ""),
                      rest=exercise_data["rest"],
                      video_url=exercise_data["video_url"],
                      day=exercise_data["day"]
                  )
                  for week in range(1, 5):
                      Evolution.objects.create(
                          exercise=exercise,
                          week_number=week,
                          description=""
                      )

            return Response(TrainerStudentProgramSerializer(instance).data, status=status.HTTP_200_OK)



class TrainerExerciseListView(generics.ListAPIView):
      serializer_class = ExerciseListSerializer
      permission_classes = [IsAuthenticated]

      def get_queryset(self):
            user = self.request.user
            if user.is_trainer:
                  return Exercise.objects.filter(program__trainer=user)
            return Exercise.objects.none()