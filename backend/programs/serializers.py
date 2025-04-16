from rest_framework import serializers
from .models import ReadyProgram, TrainerStudentProgram, Exercise ,ReadyExercise , Evolution
from users.serializers import UserSerializer

class EvolutionSerializer(serializers.ModelSerializer):
      class Meta:
            model = Evolution
            fields = ['id','week_number', 'description']

class ExerciseSerializer(serializers.ModelSerializer):
      evolutions = EvolutionSerializer(many=True, read_only=True)
      class Meta:
            model = Exercise
            fields = ['id', 'program','title', 'sets_reps', 'intensity', 'tempo', 'rest', 'video_url', 'day','evolutions']
            
        
class TrainerStudentProgramSerializer(serializers.ModelSerializer):
      trainer = UserSerializer(read_only=True)
      student = UserSerializer(read_only=True)
      exercises = ExerciseSerializer(many=True, read_only=True)
      class Meta:
            model = TrainerStudentProgram
            fields = ['id', 'trainer', 'student', 'title', 'start_date', 'end_date', 'exercises']
        
        
class ReadyExerciseSerializer(serializers.ModelSerializer):
      class Meta:
            model = ReadyExercise
            fields = ['id', 'title', 'sets_reps', 'intensity', 'tempo', 'rest', 'day']

class ReadyProgramSerializer(serializers.ModelSerializer):
      exercises = ReadyExerciseSerializer(many=True, read_only=True)

      class Meta:
            model = ReadyProgram
            fields = ['id', 'subplan', 'title', 'exercises']
            
            
class ExerciseListSerializer(serializers.ModelSerializer):
      class Meta:
            model = Exercise
            fields = ('id','title','sets_reps','intensity', 'tempo', 'rest', 'video_url', 'day')