from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from subplans.models import SubPlan

User = get_user_model()

class TrainerStudentProgram(models.Model):
      trainer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_trainer': True}, related_name='trainer_programs')
      student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_trainer': False}, related_name='student_programs')
      title = models.CharField(max_length=255)
      start_date = models.DateTimeField(default=timezone.now)
      end_date = models.DateTimeField(null=True, blank=True)

      def save(self, *args, **kwargs):
            if not self.end_date:
                  self.end_date = self.start_date + timedelta(days=30)
            super(TrainerStudentProgram, self).save(*args, **kwargs)

      def __str__(self):
            return f'{self.trainer.email} - {self.student.email}'
    
class Exercise(models.Model):
      program = models.ForeignKey(TrainerStudentProgram, on_delete=models.CASCADE, related_name='exercises')
      title = models.CharField(max_length=255)
      sets_reps = models.CharField(max_length=255)
      intensity = models.CharField(max_length=255)
      tempo = models.CharField(max_length=255, blank=True, null=True)
      rest = models.CharField(max_length=255)
      video_url = models.URLField()
      day = models.CharField(max_length=50)

      def __str__(self):
            return self.title

class Evolution(models.Model):
      exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='evolutions')
      week_number = models.PositiveIntegerField()
      description = models.TextField()

      def __str__(self):
            return f'Week {self.week_number} - {self.exercise}'

### ready programs

class ReadyProgram(models.Model):
      subplan = models.ForeignKey(SubPlan, on_delete=models.CASCADE)
      title = models.CharField(max_length=255)
      
      def __str__(self) -> str:
            return self.title

class ReadyExercise(models.Model):
      program = models.ForeignKey(ReadyProgram, on_delete=models.CASCADE,related_name='exercises')
      title = models.CharField(max_length=255)
      sets_reps = models.CharField(max_length=255)
      intensity = models.CharField(max_length=255)
      tempo = models.CharField(max_length=255)
      rest = models.CharField(max_length=255)
      video_url = models.URLField(blank=True, null=True)
      day = models.CharField(max_length=50)
      
      def __str__(self) -> str:
            return self.title